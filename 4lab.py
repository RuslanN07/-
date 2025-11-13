import numpy as np
import matplotlib.pyplot as plt

def load_matrix(path):
    return np.loadtxt(path, dtype=float)

def count_min_in_odd_cols(C):
    odd_cols = C[:, 0::2]
    return np.sum(odd_cols == np.min(odd_cols))

def count_max_in_even_rows(C):
    even_rows = C[1::2, :]
    return np.sum(even_rows == np.max(even_rows))

def build_F(A):
    n = A.shape[0]
    h = n // 2
    E = A[:h, :h].copy()
    B = A[:h, h:].copy()
    C = A[h:, h:].copy()
    F = A.copy()
    
    cnt_min = count_min_in_odd_cols(C)
    cnt_max = count_max_in_even_rows(C)
    print(f"Количество минимальных в нечетных столбцах C: {cnt_min}")
    print(f"Количество максимальных в четных строках C: {cnt_max}")
    
    if cnt_min > cnt_max:
        print("Меняем B и C симметрично")
        F[:h, h:], F[h:, h:] = C, B
    else:
        print("Меняем E и C несимметрично")
        F[:h, :h], F[h:, h:] = C, E
    
    return F

def main():
    K = int(input("Введите коэффициент K: "))
    A = load_matrix("matrix-2.txt")
    n = A.shape[0]
    assert n % 2 == 0, "Размер A должен быть чётным"
    
    print("\nМатрица A:")
    print(np.round(A, 3))
    
    F = build_F(A)
    print("\nМатрица F:")
    print(np.round(F, 3))
    
    detA = np.linalg.det(A)
    traceF = np.trace(F)
    detF = np.linalg.det(F)
    print(f"\ndet(A) = {detA:.3f}, trace(F) = {traceF:.3f}, det(F) = {detF:.3f}")
    
    
    if abs(detF) < 1e-10:
        print("ОШИБКА: матрица F вырожденная (det(F) ≈ 0), инверсия невозможна!")
        return
    
    if detA > traceF:
        print("det(A) > trace(F) → вычисляем A⁻¹·A − K·F")
        
        R = np.eye(n) - K * F
    else:
        print("det(A) ≤ trace(F) → вычисляем (Aᵀ + Gᵀ − F⁻¹)·K")
        G = np.tril(A)
        R = (A.T + G.T - np.linalg.inv(F)) * K
    
    R = np.round(R, 3)
    print("\nРезультирующая матрица R:")
    print(R)
    
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.title("Теплокарта матрицы A")
    im1 = plt.imshow(A, cmap="viridis")
    plt.colorbar(im1, label="Значения A")
    
    plt.subplot(2, 2, 2)
    diagF = np.diag(F)
    plt.title("Диагональные элементы матрицы F")
    plt.bar(range(n), diagF, color='skyblue')
    plt.xlabel("Индекс элемента")
    plt.ylabel("F[i,i]")
    
    plt.subplot(2, 2, 3)
    plt.title("Теплокарта матрицы R")
    im2 = plt.imshow(R, cmap="plasma")
    plt.colorbar(im2, label="Значения R")
    
    plt.subplot(2, 2, 4)
    row_sums = R.sum(axis=1)
    plt.title("Суммы элементов по строкам матрицы R")
    plt.plot(range(n), row_sums, marker="o", color='green')
    plt.xlabel("Номер строки")
    plt.ylabel("Сумма строки")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
