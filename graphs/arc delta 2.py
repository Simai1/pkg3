from cProfile import label

import numpy as np
import matplotlib.pyplot as plt

L = np.array([0.78, 1.57, 2.35, 3.14, 3.92, 4.71, 5.49])

t_A = np.array([33.33, 38.46, 50.0, 33.33, 34.33, 38.75, 34.41, ])

t_B = np.array([0, 15.38, 26.32, 31.48, 46.27, 57.5, 65.59, ])

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(L, t_A, label='Алгоритм A', marker='o', color='blue')
plt.plot(L, t_B, label='Алгоритм B', marker='o', color='orange')

# Настраиваем график
plt.title('Зависимость значений разности результата растеризации от длины дуги (Исп. 2)')
plt.xlabel('Длина дуги')
plt.ylabel('Разность результата растеризации')
plt.legend()
plt.grid(True)

# Устанавливаем диапазоны осей
plt.xlim(min(L) - 0.5, max(L) + 0.5)
plt.ylim(0, max(max(t_A), max(t_B)) + 0.0001)

# Показываем график
plt.show()
