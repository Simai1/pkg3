from cProfile import label

import numpy as np
import matplotlib.pyplot as plt

L = np.array([1.04, 2.09, 3.14, 4.19, 5.24, 6.28, 7.33])

t_A = np.array([25.0, 29.41, 42.31, 29.17, 25.56, 29.25, 29.03])

t_B = np.array([0, 17.65, 19.23, 30.56, 46.67, 54.72, 66.13])

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(L, t_A, label='Алгоритм A', marker='o', color='blue')
plt.plot(L, t_B, label='Алгоритм B', marker='o', color='orange')

# Настраиваем график
plt.title('Зависимость значений разности результата растеризации от длины дуги (Исп. 1)')
plt.xlabel('Длина дуги')
plt.ylabel('Разность результата растеризации')
plt.legend()
plt.grid(True)

# Устанавливаем диапазоны осей
plt.xlim(min(L) - 0.5, max(L) + 0.5)
plt.ylim(0, max(max(t_A), max(t_B)) + 0.0001)

# Показываем график
plt.show()
