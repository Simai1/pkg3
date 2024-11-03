import math
import time

import pygame

from config import *

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Запоминаем время начала выполнения
        result = func(*args, **kwargs)  # Вызываем переданную функцию
        end_time = time.time()  # Запоминаем время окончания выполнения
        execution_time = end_time - start_time  # Вычисляем время выполнения
        print(f'Время выполнения функции {func.__name__}: {execution_time:.6f} секунд')
        return result  # Возвращаем результат вызова функции
    return wrapper

@timer
def algorithm_reference_round(pixel_map, center, radius, outline_color):
    time.sleep(0.001)
    t1 = time.time()
    # Алгоритм Брезенхема для построения окружности
    x = 0
    y = radius
    d = 3 - 2 * radius  # Начальное значение d

    while x <= y:
        time.sleep(0.001)
        # Обрабатываем 8 симметричных точек
        points = [
            (center[0] + x, center[1] + y),
            (center[0] + y, center[1] + x),
            (center[0] - x, center[1] + y),
            (center[0] - y, center[1] + x),
            (center[0] + x, center[1] - y),
            (center[0] + y, center[1] - x),
            (center[0] - x, center[1] - y),
            (center[0] - y, center[1] - x)
        ]

        for px, py in points:
            if 0 <= px < len(pixel_map[0]) and 0 <= py < len(pixel_map):
                pixel_map[py][px] = outline_color  # Используем цвет контура
                # pygame.time.delay(DELAY_MS)  # Задержка между точками

        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10  # Если d > 0, уменьшаем y
        else:
            d += 4 * x + 6  # Если d <= 0, не меняем y
    t2 = time.time()

@timer
def algorithm_reference_fill(pixel_map, center, radius, new_color, outline_color):
    time.sleep(0.001)
    # global flag1
    x = center[1]
    y = center[0]
    """Заполняет область, начиная с пикселя (x, y) новым цветом."""
    stack = [(x, y)]
    old_color = pixel_map[x][y]  # Получаем цвет текущего пикселя (RGB)

    while stack:
        x, y = stack.pop()
        current_color = pixel_map[x][y]

        # Если цвет текущего пикселя совпадает со старым цветом, меняем его
        if current_color != new_color and current_color != outline_color:
            # screen.set_at((x, y), new_color)  # Меняем цвет текущего пикселя

            # Добавляем соседние пиксели в стек
            # print(center[0] - x, center[1] - y, radius ** 2)
            if x + 1 < WIDTH and y + 1 < HEIGHT and not (
                    pixel_map[x + 1][y] == outline_color and pixel_map[x][y + 1] == outline_color):
                pixel_map[x][y] = new_color
                stack.append((x + 1, y + 1))  # Право Вниз
                # print("Вправо Вниз")
            if x + 1 < WIDTH and y - 1 >= 0 and not (
                    pixel_map[x + 1][y] == outline_color and pixel_map[x][y - 1] == outline_color):
                pixel_map[x][y] = new_color
                stack.append((x + 1, y - 1))  # Вправо Вверх
                # print("Вправо Вверх")
            if x - 1 >= 0 and y + 1 < HEIGHT and not (
                    pixel_map[x - 1][y] == outline_color and pixel_map[x][y + 1] == outline_color):
                pixel_map[x][y] = new_color
                stack.append((x - 1, y + 1))  # Влево Вниз
                # print("Влево Вниз")
            if x - 1 >= 0 and y - 1 >= 0 and not (
                    pixel_map[x - 1][y] == outline_color and pixel_map[x][y - 1] == outline_color):
                pixel_map[x][y] = new_color
                stack.append((x - 1, y - 1))  # Влево Вверх
                # print("Влево Вниз")
            if x + 1 < WIDTH:
                pixel_map[x][y] = new_color
                stack.append((x + 1, y))  # Право
            if x - 1 >= 0:
                pixel_map[x][y] = new_color
                stack.append((x - 1, y))  # Лево
            if y + 1 < HEIGHT:
                pixel_map[x][y] = new_color
                stack.append((x, y + 1))  # Вниз
            if y - 1 >= 0:
                pixel_map[x][y] = new_color
                stack.append((x, y - 1))  # Вверх

            # pygame.time.delay(DELAY_MS)

@timer
def algorithm_A_round(pixel_map, center, radius, outline_color):
    time.sleep(0.001)
    # Алгоритм растеризации окружности «А» для рисования контура
    for x in range(-radius, radius + 1):  # Проходим по x от -R до R
        y_squared = radius ** 2 - x ** 2  # Вычисляем y^2
        if y_squared >= 0:  # Убедимся, что под корнем не отрицательное значение
            y = int(math.sqrt(y_squared))  # Вычисляем y как положительное значение

            # Обрабатываем 8 симметричных точек
            points = [
                (center[0] + x, center[1] + y),
                (center[0] + y, center[1] + x),
                (center[0] - x, center[1] + y),
                (center[0] - y, center[1] + x),
                (center[0] + x, center[1] - y),
                (center[0] + y, center[1] - x),
                (center[0] - x, center[1] - y),
                (center[0] - y, center[1] - x)
            ]

            for px, py in points:
                if 0 <= px < len(pixel_map[0]) and 0 <= py < len(pixel_map):
                    pixel_map[py][px] = outline_color  # Используем цвет контура
                    # pygame.time.delay(DELAY_MS)  # Задержка между точками

@timer
def algorithm_A_fill(pixel_map, center, radius, new_color, outline_color):
    time.sleep(0.001)
    # global flag1
    x = center[1]
    y = center[0]
    """Заполняет область, начиная с пикселя (x, y) новым цветом."""
    stack = [(x, y)]
    old_color = pixel_map[x][y]  # Получаем цвет текущего пикселя (RGB)

    while stack:
        x, y = stack.pop()
        current_color = pixel_map[x][y]
        # print(x, y)

        # Если цвет текущего пикселя совпадает со старым цветом, меняем его
        if current_color != new_color and current_color != outline_color:
            # screen.set_at((x, y), new_color)  # Меняем цвет текущего пикселя
            pixel_map[x][y] = new_color
            # Добавляем соседние пиксели в стек
            if x + 1 < WIDTH:
                stack.append((x + 1, y))  # Право
            if x - 1 >= 0:
                stack.append((x - 1, y))  # Лево
            if y + 1 < HEIGHT:
                stack.append((x, y + 1))  # Вниз
            if y - 1 >= 0:
                stack.append((x, y - 1))  # Вверх
                # if flag1:
                # pygame.display.flip()
                # pygame.time.delay(DELAY_MS)
    # flag1 = False

@timer
def algorithm_B_round(pixel_map, center, radius, outline_color):
    time.sleep(0.001)
    # Алгоритм растеризации окружности (дуги) «Б» для рисования контура
    for angle in range(0, 360):  # Изменение угла от 0 до 360 градусов
        rad = math.radians(angle)  # Преобразование градусов в радианы
        x = int(center[0] + radius * math.cos(rad))
        y = int(center[1] + radius * math.sin(rad))
        # pygame.display.flip()
        # Проверяем, не выходит ли точка за границы карты пикселей
        if 0 <= x < len(pixel_map[0]) and 0 <= y < len(pixel_map):
            pixel_map[y][x] = outline_color  # Используем цвет контура
            # pygame.display.flip()
            # pygame.time.delay(DELAY_MS)  # Задержка между точками

@timer
def algorithm_B_fill(pixel_map, center, radius, fill_color, outline_color):
    time.sleep(0.001)
    # Заливка круговой области построчно, начиная от центра строки
    for y in range(-radius, radius + 1):
        # Вычисляем максимальное смещение по x для текущей строки y
        x_limit = int(math.sqrt(radius ** 2 - y ** 2))

        # Начинаем заливку с центра строки и двигаемся влево и вправо
        for direction in [-1, 1]:  # Сначала влево, затем вправо
            x = 0
            while abs(x) <= x_limit:
                pixel_x = center[0] + x * direction
                pixel_y = center[1] + y

                # Проверяем, что координаты пикселя находятся в пределах экрана
                if 0 <= pixel_x < len(pixel_map[0]) and 0 <= pixel_y < len(pixel_map):
                    # if pixel_map[pixel_y][pixel_x] == outline_color:
                    #     break  # Прерываем заливку, если достигли контура
                    pixel_map[pixel_y][pixel_x] = fill_color  # Заполняем пиксель цветом заливки

                x += 1  # Переходим к следующему пикселю влево или вправо

        #         pygame.display.flip()
        # pygame.display.flip()
        # pygame.time.delay(DELAY_MS * 50)