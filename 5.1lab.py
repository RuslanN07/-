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
    sums = [(x, sum(int(d) for d in str(x))) for x in xs]
    if not sums:
        return [], 0
    max_sum = max(s for _, s in sums)
    return [x for x, s in sums if s == max_sum], max_sum

def main():
    n = 1000

    algo_list = generate_algo(n)
    py_list = generate_python(n)
    print(f"n = {n} (считаем от 1 до этого числа)")
    print("\nАлгоритмический метод — первые 10 чисел:", algo_list[:10])
    print("Product метод — первые 10 чисел:", py_list[:10])
    print("\nВсего чисел:", len(py_list))

    t1 = timeit.timeit(lambda: generate_algo(n), number=100)
    t2 = timeit.timeit(lambda: generate_python(n), number=100)
    print(f"\nВремя (100 повторов): алгоритмический = {t1:.4f}s, python = {t2:.4f}s")

    cons = generate_constrained(n)
    optimal, max_sum = find_optimal(cons)
    print("\nЧисла, кратные 3 (ограничение) и с 2–3 четными цифрами — всего:", len(cons))
    print(f"\nОптимальные числа (максимальная сумма цифр = {max_sum}): {optimal}")

if __name__ == "__main__":
    main()
