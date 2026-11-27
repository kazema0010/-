from datetime import datetime
from PIL import Image, ImageFilter, ImageStat

INPUT_DIR = "Lab2_Media/data/input/"
OUTPUT_PATH = "Lab2_Media/data/output/result.jpg"
LOG_PATH = "Lab2_Media/logs/history.txt"
FILTER_NAME = "Фильтр Гаусса + цветокоррекция по шаблону"


def write_log(file_name, status):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    line = "[" + now + "] Файл: " + file_name + " | Фильтр: " + FILTER_NAME + " | Статус: " + status + "\n"
    with open(LOG_PATH, "a", encoding="UTF-8") as log:
        log.write(line)

def color_correction(img, template):
    mean_img = ImageStat.Stat(img).mean
    std_img = ImageStat.Stat(img).stddev
    mean_tpl = ImageStat.Stat(template).mean
    std_tpl = ImageStat.Stat(template).stddev

    table = []
    for c in range(3):
        for v in range(256):
            if std_img[c] == 0:
                new_v = mean_tpl[c]
            else:
                new_v = (v - mean_img[c]) * std_tpl[c] / std_img[c] + mean_tpl[c]
            new_v = max(0, min(255, int(new_v)))
            table.append(new_v)

    return img.point(table)


def main():
    file_name = input("Какой файл обработать (image1.jpg или image2.png)? ")
    path = INPUT_DIR + file_name

    if file_name == "image1.jpg":
        template_name = "image2.png"
    else:
        template_name = "image1.jpg"

    try:
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

    img = img.filter(ImageFilter.GaussianBlur(radius=3))

    img = color_correction(img, template)

    img.save(OUTPUT_PATH)
    print("Готово! Результат сохранён в " + OUTPUT_PATH)

    write_log(file_name, "Успешно")


main()
