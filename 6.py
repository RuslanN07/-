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
    F = [0]*(n+1)
    fac = 1
    for i in range(n+1):
        if i == 0:
            F[i] = 1
        elif i == 1:
            F[i] = 2
        else:
            fac *= (2*i-1)*(2*i)
            if i <= 15:
                F[i] = F[i-2] + F[i-1]
            else:
                sign = 1 if i % 2 == 0 else -1
                F[i] = sign * (5*F[i-1]/fac - 7*(i-2))
    return F[n]

results = [
    (
        n,
        timeit.timeit(lambda n=n: F_recursive(n), number=10),
        timeit.timeit(lambda n=n: F_iterative(n), number=10)
    )
    for n in range(2, 31)
]

df = pd.DataFrame(results, columns=['n', 'Recursive (s)', 'Iterative (s)'])
print(df.to_string(index=False))

plt.figure(figsize=(8,5))
plt.plot(df['n'], df['Recursive (s)'], '--o', label='Рекурсивно')
plt.plot(df['n'], df['Iterative (s)'], '-o', label='Итеративно')
plt.xlabel('n')
plt.ylabel('Время, с')
plt.title('Сравнение производительности')
plt.legend()
plt.grid(True)
plt.show()
