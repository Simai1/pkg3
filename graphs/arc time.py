from cProfile import label

import numpy as np
import matplotlib.pyplot as plt

L = np.array([ 0.78,  1.04,  1.04,  1.57,  2.09,  2.09,  2.35,  2.61,
                      3.14,  3.14,  3.14,  3.14,  3.92,  4.19,  4.19,
                      4.71,  5.23,  5.24,  5.24,  5.49,  6.28,  6.28,
                      6.28,  7.33,  7.33,  7.85,  9.42, 10.47, 12.56,
                     13.08, 15.7 , 15.7 , 18.32, 18.84, 21.99])

t_A = np.array([0.000126, 0.000127, 0.000130, 0.000221, 0.000222,
                       0.000250, 0.000331, 0.000147, 0.000331, 0.000342,
                       0.000429, 0.000190, 0.000532, 0.000445, 0.000440,
                       0.000638, 0.000262, 0.000556, 0.000540, 0.000738,
                       0.000727, 0.000647, 0.000278, 0.000775, 0.000808,
                       0.000399, 0.000417, 0.000529, 0.000539, 0.000766,
                       0.001172, 0.001310, 0.000978, 0.000793, 0.000914])

t_B = np.array([0.000025, 0.000032, 0.000033, 0.000021, 0.000028,
                       0.000028, 0.000020, 0.000073, 0.000027, 0.000028,
                       0.000020, 0.000084, 0.000021, 0.000026, 0.000027,
                       0.000021, 0.000068, 0.000026, 0.000027, 0.000066,
                       0.000066, 0.000096, 0.000026, 0.000027, 0.000081,
                       0.000080, 0.000079, 0.000079, 0.000028, 0.000028,
                       0.000026, 0.000026, 0.000026, 0.000026, 0.000026])

t_R = np.array([0.000092, 0.000098, 0.000215, 0.000089, 0.000091,
                       0.000098, 0.000121, 0.000120, 0.000133, 0.000131,
                       0.000166, 0.000113, 0.000200, 0.000172, 0.000209,
                       0.000237, 0.000104, 0.000208, 0.000232, 0.000257,
                       0.000297, 0.000319, 0.000116, 0.000344, 0.000344,
                       0.000396, 0.000456, 0.000286, 0.000172, 0.000208,
                       0.000254, 0.000190, 0.000275, 0.000290, 0.000286])

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(L, t_A, label='Алгоритм A', marker='o', color='blue')
plt.plot(L, t_B, label='Алгоритм B', marker='o', color='orange')
plt.plot(L, t_R, label='Эталонный алгоритм', marker='o', color='red')

# Настраиваем график
plt.title('Зависимость затраченного времени t от длины дуги L')
plt.xlabel('Длина дуги L')
plt.ylabel('Затраченное время t (в секундах)')
plt.legend()
plt.grid(True)

# Устанавливаем диапазоны осей
plt.xlim(min(L) - 0.5, max(L) + 0.5)
plt.ylim(0, max(max(t_A), max(t_B)) + 0.0001)

# Показываем график
plt.show()