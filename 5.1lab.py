import timeit
from itertools import product

def count_even_digits(x):
    return sum(1 for d in str(x) if int(d) % 2 == 0)

def generate_algo(n):
    result = []
    for x in range(1, n + 1):
        c = count_even_digits(x)
        if 2 <= c <= 3:
            result.append(x)
    return result

def generate_python(n):
    return [x for x in range(1, n + 1) if 2 <= count_even_digits(x) <= 3]

def generate_constrained(n):
    return [x for x in range(1, n + 1) if x % 3 == 0 and 2 <= count_even_digits(x) <= 3]

def find_optimal(xs):
    if not xs:
        return [], 0
    sums = [(x, sum(int(d) for d in str(x))) for x in xs]
    max_sum = max(s for _, s in sums)
    optimal = [x for x, s in sums if s == max_sum]
    return sorted(optimal), max_sum  

def main():
    n = 1000
    print(f"Анализируем числа от 1 до {n}\n" + "="*50)

    algo_list = generate_algo(n)
    py_list = generate_python(n)
    cons_list = generate_constrained(n)

    print(f"Найдено чисел с 2–3 чётными цифрами: {len(py_list)} шт.\n")
    print("ВСЕ такие числа:")
    print(py_list)
    print("\n" + "-"*50)

    print(f"\nИз них кратны 3: {len(cons_list)} шт.")
    print("Числа, кратные 3 и с 2–3 чётными цифрами:")
    print(cons_list)

    optimal, max_sum = find_optimal(cons_list)
    print(f"\n\nОптимальные числа (максимальная сумма цифр среди кратных 3):")
    print(f"Сумма цифр = {max_sum}")
    print(f"Таких чисел: {len(optimal)}")
    print("Список:", optimal)

    print("\n" + "="*50)
    print("Сравнение скорости (100 запусков):")
    t1 = timeit.timeit(lambda: generate_algo(n), number=100)
    t2 = timeit.timeit(lambda: generate_python(n), number=100)
    print(f"Алгоритмический подход: {t1:.4f} сек")
    print(f"Списковое включение (Pythonic): {t2:.4f} сек")
    print(f"→ {'Списковое включение' if t2 < t1 else 'Цикл'} быстрее в {abs(t1/t2 - 1)*100:.1f}% случаев")

if __name__ == "__main__":
    main()
