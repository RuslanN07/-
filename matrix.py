def read_matrix(path):
    with open(path, "r") as f:
        return [list(map(int, line.split())) for line in f]

def print_matrix(M, name):
    print(f"\n{name}:")
    for row in M:
        print(" ".join(f"{x:4}" for x in row))

def transpose(A):
    return [list(row) for row in zip(*A)]

def mul(A, B):
    n = len(A)
    return [
        [sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]

def scalar_mult(K, M):
    return [[K * x for x in row] for row in M]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def get_regions(n):
    r1 = [(i,j) for i in range(n) for j in range(n) if i<j and i+j< n-1]
    r2 = [(i,j) for i in range(n) for j in range(n) if i<j and i+j> n-1]
    r3 = [(i,j) for i in range(n) for j in range(n) if i>j and i+j> n-1]
    r4 = [(i,j) for i in range(n) for j in range(n) if i>j and i+j< n-1]
    return r1, r2, r3, r4

def build_F(A):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)

    # вычисление критериев
    sum_odd_cols_r2 = sum(A[i][j] for i,j in r2 if j % 2 == 1)
    prod_even_cols_r1 = 1
    for i,j in r1:
        if j % 2 == 0:
            prod_even_cols_r1 *= A[i][j]

    print(f"Критерии для перестановки областей:")
    print(f"  Сумма чисел в НЕчетных столбцах области 2: {sum_odd_cols_r2}")
    print(f"  Произведение чисел в четных столбцах области 1: {prod_even_cols_r1}")

    if sum_odd_cols_r2 > prod_even_cols_r1:
        print("Решение: симметрично меняем области 2 и 3\n")
        for (i2,j2), (i3,j3) in zip(r2, r3):
            F[i2][j2], F[i3][j3] = F[i3][j3], F[i2][j2]
    else:
        print("Решение: несимметрично меняем области 1 и 2\n")
        for (i1,j1), (i2,j2) in zip(r1, r2):
            F[i1][j1], F[i2][j2] = F[i2][j2], F[i1][j1]

    return F

def main():
    K = int(input("Введите K: "))
    A = read_matrix("matrix.txt")
    print_matrix(A, "Матрица A")

    F = build_F(A)  # внутри функции выведутся критерии и способ обмена
    print_matrix(F, "Матрица F")

    KA = scalar_mult(K, A)
    KAT = scalar_mult(K, transpose(A))
    R = sub(mul(KA, A), KAT)
    print_matrix(R, "(K*A)*A − K*AT")

if __name__ == "__main__":
    main()
