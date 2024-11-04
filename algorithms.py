import math
import time
import timeit
import pygame

from config import *


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()  # Запоминаем время начала выполнения
        result = func(*args, **kwargs)  # Вызываем переданную функцию
        end_time = timeit.default_timer()  # Запоминаем время окончания выполнения
        execution_time = end_time - start_time  # Вычисляем время выполнения
        print(f'Время выполнения функции {func.__name__}: {execution_time:.6f} секунд')
        return result  # Возвращаем результат вызова функции

    return wrapper


@timer
def algorithm_reference_round(pixel_map, center, radius, outline_color, angle_start=0, angle_end=360):
    # Преобразуем углы в радианы и нормализуем
    angle_start = math.radians(angle_start % 360)
    if angle_end == 360:
        angle_end = 2 * math.pi
    else:
        angle_end = math.radians(angle_end % 360)

    def is_within_angle(x, y):
        """Проверка, находится ли точка (x, y) в пределах заданного углового диапазона."""
        angle = math.atan2(y, x)
        if angle < 0:
            angle += 2 * math.pi

        # Если угол задан как полный круг, разрешаем все точки
        if angle_start == 0 and angle_end == 2 * math.pi:
            return True

        if angle_start <= angle_end:
            return angle_start <= angle <= angle_end
        else:
            return angle >= angle_start or angle <= angle_end

    x = 0
    y = radius
    d = 3 - 2 * radius  # Начальное значение для алгоритма Брезенхема

    while x <= y:
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

        # Проверяем каждую точку на соответствие угловому диапазону
        for px, py in points:
            dx, dy = px - center[0], py - center[1]
            if is_within_angle(dx, dy):
                if 0 <= px < len(pixel_map[0]) and 0 <= py < len(pixel_map):
                    pixel_map[py][px] = outline_color  # Используем цвет контура

        # Обновляем параметры алгоритма Брезенхема
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6

    return pixel_map


@timer
def algorithm_reference_fill(pixel_map, center, radius, new_color, outline_color):
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
    return pixel_map


@timer
def algorithm_A_round(pixel_map, center, radius, outline_color, angle_start=0, angle_end=180):
    angle_start = math.radians(angle_start)
    angle_end = math.radians(angle_end)

    def is_within_angle(x, y):
        angle = math.atan2(y, x)
        if angle < 0:
            angle += 2 * math.pi
        return angle_start <= angle <= angle_end

    for x in range(-radius, radius + 1):
        y_squared = radius ** 2 - x ** 2
        if y_squared >= 0:
            y = int(math.sqrt(y_squared))

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
                dx, dy = px - center[0], py - center[1]
                if is_within_angle(dx, dy):
                    if 0 <= px < len(pixel_map[0]) and 0 <= py < len(pixel_map):
                        if pixel_map[py][px] is None:
                            pixel_map[py][px] = tuple(255 - c for c in outline_color)
                        else:
                            pixel_map[py][px] = outline_color  # Используем цвет контура
    return pixel_map


@timer
def algorithm_A_fill(pixel_map, center, radius, new_color, outline_color):
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
    return pixel_map


@timer
def algorithm_B_round(pixel_map, center, radius, outline_color, angle_start=0, angle_end=180):
    # Алгоритм растеризации окружности (дуги) «Б» для рисования контура
    for angle in range(angle_start, angle_end):  # Изменение угла от 0 до 360 градусов
        rad = math.radians(angle)  # Преобразование градусов в радианы
        x = int(center[0] + radius * math.cos(rad))
        y = int(center[1] + radius * math.sin(rad))
        # pygame.display.flip()
        # Проверяем, не выходит ли точка за границы карты пикселей
        if 0 <= x < len(pixel_map[0]) and 0 <= y < len(pixel_map):
            # if pixel_map[y][x] is not None:
            #     pixel_map[y][x] = tuple(255 - c for c in outline_color)
            # else:
            pixel_map[y][x] = outline_color  # Используем цвет контура
            # pygame.display.flip()
            # pygame.time.delay(DELAY_MS)  # Задержка между точками
    return pixel_map


@timer
def algorithm_B_fill(pixel_map, center, radius, fill_color, outline_color):
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
    return pixel_map


def bresenham_line(x0, y0, x1, y1, pixel_map, color):
    """Алгоритм Брезенхема для рисования линии."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < len(pixel_map) and 0 <= y0 < len(pixel_map[0]):
            pixel_map[y0][x0] = color

        if x0 == x1 and y0 == y1:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x0 += sx
        if err2 < dx:
            err += dx
            y0 += sy


def draw_rounded_rect(pixel_map, center, w, h, outline_color):
    radius = int(math.sqrt(w ** 2 + h ** 2) // 2)
    radius -= int(radius * 0.1)
    # algorithm_reference_round(pixel_map, center, radius, outline_color)

    # line 1
    line_y = center[1] - h // 2
    intersections_bottom = find_circle_line_intersection(center, radius, line_slope=0, line_intercept=line_y)
    tr, tl = find_angles_on_circle(center, intersections_bottom)
    # line 2
    line_y = center[1] + h // 2
    intersections_upper = find_circle_line_intersection(center, radius, line_slope=0, line_intercept=line_y)
    br, bl = find_angles_on_circle(center, intersections_upper)
    # line 3
    line_x = center[0] - w // 2  # x-координата левой линии
    intersections_left = find_circle_line_intersection(center, radius, vertical_x=line_x)
    lb, lt = find_angles_on_circle(center, intersections_left)
    # line 4 (правую вертикальную линию)
    line_x = center[0] + w // 2  # x-координата правой линии
    intersections_right = find_circle_line_intersection(center, radius, vertical_x=line_x)
    rb, rt = find_angles_on_circle(center, intersections_right)

    algorithm_reference_round(pixel_map, center, radius+1, outline_color, tr, rt)
    algorithm_reference_round(pixel_map, center, radius+1, outline_color, lt, tl)
    algorithm_reference_round(pixel_map, center, radius+1, outline_color, bl, lb)
    algorithm_reference_round(pixel_map, center, radius+1, outline_color, rb, br)

    bresenham_line(intersections_bottom[0][0], intersections_bottom[0][1],
                   intersections_bottom[1][0], intersections_bottom[1][1], pixel_map, outline_color)
    bresenham_line(intersections_upper[0][0], intersections_upper[0][1],
                   intersections_upper[1][0], intersections_upper[1][1], pixel_map, outline_color)
    bresenham_line(intersections_left[0][0], intersections_left[0][1],
                   intersections_left[1][0], intersections_left[1][1], pixel_map, outline_color)
    bresenham_line(intersections_right[0][0], intersections_right[0][1],
                   intersections_right[1][0], intersections_right[1][1], pixel_map, outline_color)


def find_circle_line_intersection(center, radius, line_slope=None, line_intercept=None, vertical_x=None):
    x_center, y_center = center
    intersections = []

    # Обработка горизонтальной линии
    if line_slope is not None and line_intercept is not None:
        # Уравнение линии: y = mx + b
        # Решаем уравнение окружности: (x - x_center)^2 + (y - y_center)^2 = radius^2
        # Подставляем y из уравнения линии
        m = line_slope
        b = line_intercept
        a = 1 + m ** 2
        b_coef = 2 * (m * (b - y_center) - x_center)
        c = x_center ** 2 + (b - y_center) ** 2 - radius ** 2

        # Вычисляем дискриминант
        discriminant = b_coef ** 2 - 4 * a * c

        if discriminant >= 0:
            # Найдем x-координаты пересечений
            x1 = (-b_coef + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b_coef - math.sqrt(discriminant)) / (2 * a)

            # Найдем соответствующие y-координаты
            y1 = m * x1 + b
            y2 = m * x2 + b

            intersections.append((round(x1), round(y1)))
            intersections.append((round(x2), round(y2)))

    # Обработка вертикальной линии
    if vertical_x is not None:
        # Уравнение вертикальной линии: x = vertical_x
        # Подставляем x в уравнение окружности
        a = vertical_x - x_center
        h = math.sqrt(radius ** 2 - a ** 2)

        if not math.isnan(h):  # Если h является действительным числом
            intersections.append((round(vertical_x), round(y_center + h)))
            intersections.append((round(vertical_x), round(y_center - h)))

    return intersections


def find_angles_on_circle(center, points):
    """
    Находит углы, образуемые точками относительно центра окружности.

    Args:
    - center: tuple (x_center, y_center) - центр окружности.
    - points: list of tuples [(x1, y1), (x2, y2)] - точки на окружности.

    Returns:
    - list of floats: углы в градусах.
    """
    angles = []
    x_center, y_center = center

    for point in points:
        x, y = point
        # Вычисляем угол в радианах
        angle_rad = math.atan2(y - y_center, x - x_center)
        # Преобразуем в градусы
        angle_deg = math.degrees(angle_rad)
        angles.append(angle_deg)

    return angles