import tkinter as tk
import math

def press(s):
    entry.insert(tk.END, s)

def clear():
    entry.delete(0, tk.END)

def show(text):
    clear()
    entry.insert(0, text)

def equals():
    try:
        show(eval(entry.get()))
    except Exception:
        show("Ошибка")

def sin():
    try:
        x = float(entry.get())
        show(round(math.sin(math.radians(x)), 8))
    except ValueError:
        show("Ошибка")

root = tk.Tk()
root.title("Калькулятор")

entry = tk.Entry(root, font=("Arial", 18), justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("+", 4, 3),
]
for text, r, c in buttons:
    tk.Button(root, text=text, width=5, height=2,
              command=lambda t=text: press(t)).grid(row=r, column=c)

tk.Button(root, text="=", width=5, height=2, command=equals).grid(row=4, column=2)
tk.Button(root, text="C", width=5, height=2, command=clear).grid(row=5, column=0)
tk.Button(root, text="sin", width=11, height=2, command=sin).grid(row=5, column=1, columnspan=2)

root.mainloop()
