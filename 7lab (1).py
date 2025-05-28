import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from itertools import product

def count_even_digits(x):
    return sum(int(d) % 2 == 0 for d in str(x))

def on_run():
    output.delete('1.0', tk.END)
    try:
        n = int(entry.get())
    except ValueError:
        output.insert(tk.END, "Ошибка: введите целое число n\n")
        return

    nums = []
    max_len = len(str(n))
    for length in range(1, max_len + 1):
        for digits in product('0123456789', repeat=length):
            if digits[0] == '0':
                continue
            x = int(''.join(digits))
            if x > n:
                continue
            c = count_even_digits(x)
            if 2 <= c <= 3:
                nums.append(x)

    output.insert(tk.END, f"Всего чисел с 2–3 четными цифрами: {len(nums)}\n")
    output.insert(tk.END, "Первые 10: " + ", ".join(map(str, nums[:10])) + "\n\n")

    cons = [x for x in nums if x % 3 == 0]
    output.insert(tk.END, f"С ограничением (x % 3 == 0): {len(cons)}\n")

    if cons:
        sums = [(x, sum(map(int, str(x)))) for x in cons]
        max_sum = max(s for _, s in sums)
        optimal = [x for x, s in sums if s == max_sum]

        output.insert(tk.END, f"Оптимальные (максимальная сумма цифр = {max_sum}):\n")
        for i, x in enumerate(optimal, 1):
            end = ", " if i % 5 and i != len(optimal) else "\n"
            output.insert(tk.END, f"{x}{end}")
        output.insert(tk.END, f"\nВсего оптимальных: {len(optimal)}\n")
        output.insert(tk.END, f"Пример одного оптимального: {optimal[0]}\n")
    else:
        output.insert(tk.END, "Подходящих под ограничение нет\n")

root = tk.Tk()
root.title("Лабораторная 6, вар.10")

tk.Label(root, text="Введите n:").pack(padx=10, pady=(10,0))
entry = tk.Entry(root)
entry.pack(padx=10, pady=(0,10))
entry.insert(0, "1000")

btn = tk.Button(root, text="Запустить", command=on_run)
btn.pack(padx=10, pady=(0,10))

output = ScrolledText(root, width=60, height=20, wrap=tk.WORD)
output.pack(padx=10, pady=(0,10))

root.mainloop()
