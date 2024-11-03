from cProfile import label

import numpy as np
import matplotlib.pyplot as plt

L = np.array([1145,4801, 6657, 10953, 15413])

t_A = np.array([0.000831,0.002787 ,0.003819, 0.006378,0.008739])

t_B = np.array([0.000293,0.001073 ,0.001489, 0.002416,0.003328])

t_R = np.array([0.002999,0.011379, 0.014192, 0.035432,0.044643])

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(L, t_A, label='Алгоритм A', marker='o', color='blue')
plt.plot(L, t_B, label='Алгоритм B', marker='o', color='orange')
plt.plot(L, t_R, label='Эталонный алгоритм', marker='o', color='red')

# Настраиваем график
plt.title('Зависимость затраченного времени t от площади области S')
plt.xlabel('Площадь  области S')
plt.ylabel('Затраченное время t (в секундах)')
plt.legend()
plt.grid(True)

# Устанавливаем диапазоны осей
plt.xlim(min(L) - 0.5, max(L) + 0.5)
plt.ylim(0, max(max(t_A), max(t_R)) + 0.0001)

# Показываем график
plt.show()
