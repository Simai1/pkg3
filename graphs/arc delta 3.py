from cProfile import label

import numpy as np
import matplotlib.pyplot as plt

L = np.array([2.61, 5.23, 7.85, 10.47, 13.08, 15.7, 18.32])

t_A = np.array([31.11, 36.26, 44.12, 34.41, 33.33, 35.25, 34.06, ])

t_B = np.array([33.33, 41.76, 45.59, 55.38, 61.9, 70.14, 77.09, ])

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(L, t_A, label='Алгоритм A', marker='o', color='blue')
plt.plot(L, t_B, label='Алгоритм B', marker='o', color='orange')

# Настраиваем график
plt.title('Зависимость значений разности результата растеризации от длины дуги (Исп. 3)')
plt.xlabel('Длина дуги')
plt.ylabel('Разность результата растеризации')
plt.legend()
plt.grid(True)

# Устанавливаем диапазоны осей
plt.xlim(min(L) - 0.5, max(L) + 0.5)
plt.ylim(0, max(max(t_A), max(t_B)) + 0.0001)

# Показываем график
plt.show()
