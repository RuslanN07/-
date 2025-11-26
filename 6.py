import math
import timeit
import pandas as pd
import matplotlib.pyplot as plt

def F_recursive(n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    if 2 <= n <= 15:
        return F_recursive(n-2) + F_recursive(n-1)
    sign = 1 if n % 2 == 0 else -1
    return sign * (5 * F_recursive(n-1) / math.factorial(2*n) - 7*(n-2))

def F_iterative(n):
    if n == 0:
        return 1
    if n == 1:
        return 2

    prev_prev = 1
    prev = 2
    fac_term = 1.0

    if n <= 15:
        for i in range(2, n + 1):
            current = prev_prev + prev
            prev_prev, prev = prev, current
        return prev

    current = prev
    for k in range(2, n + 1):
        if k > 15:
            fac_term /= (2 * k) * (2 * k - 1)
            sign = 1 if k % 2 == 0 else -1
            current = sign * (5 * prev * fac_term - 7 * (k - 2))
        else:
            current = prev_prev + prev
            prev_prev = prev
        prev = current

    return current

results = []
for n in range(2, 31):
    t_rec = timeit.timeit(lambda n=n: F_recursive(n), number=10)
    t_iter = timeit.timeit(lambda n=n: F_iterative(n), number=10)
    results.append((n, t_rec, t_iter))

df = pd.DataFrame(results, columns=['n', 'Recursive (s)', 'Iterative (s)'])
print(df.to_string(index=False))

plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['Recursive (s)'], '--o', label='Рекурсивно')
plt.plot(df['n'], df['Iterative (s)'], '-s', label='Итеративно (O(1) памяти)')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('Время, с (лог. шкала)')
plt.title('Сравнение производительности')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

