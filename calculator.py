import math
import tkinter as tk


# ---------- Лексер: строка -> список токенов ----------
def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
        elif c.isdigit() or c == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(float(expr[i:j]))
            i = j
        elif c in '+-*/()':
            tokens.append(c)
            i += 1
        elif expr[i:i + 3] == 'sin':
            tokens.append('sin')
            i += 3
        else:
            raise ValueError("Неизвестный символ: " + c)
    return tokens


# ---------- Парсер (рекурсивный спуск) с вычислением по ходу разбора ----------
def calculate(expr):
    tokens = tokenize(expr)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def eat():
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError("Выражение оборвано")
        pos += 1
        return tokens[pos - 1]

    # сложение и вычитание (низший приоритет)
    def parse_expr():
        value = parse_term()
        while peek() in ('+', '-'):
            if eat() == '+':
                value += parse_term()
            else:
                value -= parse_term()
        return value

    # умножение и деление
    def parse_term():
        value = parse_factor()
        while peek() in ('*', '/'):
            if eat() == '*':
                value *= parse_factor()
            else:
                divisor = parse_factor()
                if divisor == 0:
                    raise ZeroDivisionError("Деление на ноль")
                value /= divisor
        return value

    # число, скобки, унарный минус, sin (высший приоритет)
    def parse_factor():
        t = peek()
        if t == '-':
            eat()
            return -parse_factor()
        if t == 'sin':
            eat()
            if eat() != '(':
                raise ValueError("После sin нужна скобка")
            value = parse_expr()
            if eat() != ')':
                raise ValueError("Нет закрывающей скобки")
            return math.sin(value)
        if t == '(':
            eat()
            value = parse_expr()
            if eat() != ')':
                raise ValueError("Нет закрывающей скобки")
            return value
        if isinstance(t, float):
            return eat()
        raise ValueError("Ошибка в выражении")

    result = parse_expr()
    if pos != len(tokens):
        raise ValueError("Лишние символы в выражении")
    return result


# ---------- Интерфейс ----------
def click(text):
    if text == "C":
        display.delete(0, tk.END)
    elif text == "=":
        try:
            result = format(calculate(display.get()), ".10g")  # убирает лишние разряды
        except Exception:
            result = "Ошибка"
        display.delete(0, tk.END)
        display.insert(0, result)
    else:
        display.insert(tk.END, text)


root = tk.Tk()
root.title("Калькулятор")

display = tk.Entry(root, font=("Arial", 20), justify="right")
display.grid(row=0, column=0, columnspan=4)

buttons = ["7", "8", "9", "/",
           "4", "5", "6", "*",
           "1", "2", "3", "-",
           "0", ".", "(", ")",
           "sin(", "C", "=", "+"]

for i, text in enumerate(buttons):
    tk.Button(root, text=text, font=("Arial", 16), width=5, height=2,
              command=lambda t=text: click(t)).grid(row=i // 4 + 1, column=i % 4)

root.mainloop()
