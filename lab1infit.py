import math
import tkinter as tk

root = tk.Tk()
root.title("Калькулятор")

display = tk.Entry(root, font=("Arial", 20), justify="right")
display.grid(row=0, column=0, columnspan=4)


def click(text):
    if text == "C":
        display.delete(0, tk.END)
    elif text == "=":
        try:
            result = eval(display.get(), {"__builtins__": {}}, {"sin": math.sin})
        except Exception:
            result = "Ошибка"
        display.delete(0, tk.END)
        display.insert(0, result)
    else:
        display.insert(tk.END, text)


buttons = ["7", "8", "9", "/",
           "4", "5", "6", "*",
           "1", "2", "3", "-",
           "0", ".", "(", ")",
           "sin(", "C", "=", "+"]

for i, text in enumerate(buttons):
    tk.Button(root, text=text, font=("Arial", 16), width=5, height=2,
              command=lambda t=text: click(t)).grid(row=i // 4 + 1, column=i % 4)

root.mainloop()
