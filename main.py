# Лабораторная работа №2. Вариант 47
# Задание 1: фильтр Гаусса
# Задание 2: цветокоррекция по шаблону

from datetime import datetime
from PIL import Image, ImageFilter, ImageStat

INPUT_DIR = "Lab2_Media/data/input/"
OUTPUT_PATH = "Lab2_Media/data/output/result.jpg"
LOG_PATH = "Lab2_Media/logs/history.txt"
FILTER_NAME = "Фильтр Гаусса + цветокоррекция по шаблону"


def write_log(file_name, status):
    # режим 'a' - дописываем в конец, старые записи сохраняются
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    line = "[" + now + "] Файл: " + file_name + " | Фильтр: " + FILTER_NAME + " | Статус: " + status + "\n"
    with open(LOG_PATH, "a", encoding="UTF-8") as log:
        log.write(line)


def color_correction(img, template):
    # Цветокоррекция по шаблону: подгоняем среднее и разброс (стандартное
    # отклонение) каждого канала R, G, B под шаблонное изображение
    mean_img = ImageStat.Stat(img).mean
    std_img = ImageStat.Stat(img).stddev
    mean_tpl = ImageStat.Stat(template).mean
    std_tpl = ImageStat.Stat(template).stddev

    table = []  # таблица замены яркости для всех трёх каналов (3 * 256 значений)
    for c in range(3):
        for v in range(256):
            if std_img[c] == 0:
                new_v = mean_tpl[c]
            else:
                new_v = (v - mean_img[c]) * std_tpl[c] / std_img[c] + mean_tpl[c]
            # значение должно быть от 0 до 255
            new_v = max(0, min(255, int(new_v)))
            table.append(new_v)

    return img.point(table)


def main():
    file_name = input("Какой файл обработать (image1.jpg или image2.png)? ")
    path = INPUT_DIR + file_name

    # шаблоном для цветокоррекции будет второе изображение из папки input
    if file_name == "image1.jpg":
        template_name = "image2.png"
    else:
        template_name = "image1.jpg"

    try:
        # Поиск и открытие файла
        f = open(path, "rb")
        img = Image.open(f)
        img = img.convert("RGB")
        f.close()

        t = open(INPUT_DIR + template_name, "rb")
        template = Image.open(t)
        template = template.convert("RGB")
        t.close()

    except PermissionError:
        print("Ошибка: Нет прав на чтение файла " + file_name + ". Обратитесь к администратору")
        write_log(file_name, "Ошибка доступа")
        return
    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        write_log(file_name, "Ошибка: файл не найден")
        return

    # 1. Фильтр Гаусса (сглаживание)
    img = img.filter(ImageFilter.GaussianBlur(radius=3))

    # 2. Цветокоррекция по шаблону
    img = color_correction(img, template)

    # Сохранение результата
    img.save(OUTPUT_PATH)
    print("Готово! Результат сохранён в " + OUTPUT_PATH)

    write_log(file_name, "Успешно")


main()
