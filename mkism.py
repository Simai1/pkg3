from sys import flags

import pygame
import sys
import math

# Константы
flag = True
WIDTH, HEIGHT = 1000, 1000
PIXEL_SIZE = 10
INITIAL_SCALE = 1
MAX_SCALE = 5
MIN_SCALE = 0.1
DELAY_MS = 1  # Задержка в миллисекундах между шагами


def draw_canvas(screen, scale, pixel_map, offset_x, offset_y):
    # Заливаем экран белым цветом
    screen.fill((255, 255, 255))

    # Рисуем рамки для каждого пикселя
    for y in range(0, HEIGHT // PIXEL_SIZE):
        for x in range(0, WIDTH // PIXEL_SIZE):
            # Увеличиваем размер пикселя по масштабу
            rect = pygame.Rect((x * PIXEL_SIZE * scale) + offset_x, (y * PIXEL_SIZE * scale) + offset_y,
                               PIXEL_SIZE * scale, PIXEL_SIZE * scale)
            pygame.draw.rect(screen, (192, 192, 192), rect, 1)  # Обводим серым цветом с шириной 1

            # Если пиксель активен, заливаем его цветом
            if pixel_map[y][x] is not None:  # Проверяем, не является ли цвет пустым
                pygame.draw.rect(screen, pixel_map[y][x], rect)  # Заполнение активных пикселей их цветом

    # Координаты для рисования осей, учитывая масштаб и смещение
    center_x_pixel = (WIDTH // PIXEL_SIZE) // 2
    center_y_pixel = (HEIGHT // PIXEL_SIZE) // 2
    center_x = center_x_pixel * PIXEL_SIZE * scale + offset_x
    center_y = center_y_pixel * PIXEL_SIZE * scale + offset_y

    # Рисуем оси
    pygame.draw.line(screen, (0, 0, 0), (0, center_y), (WIDTH, center_y), 2)  # Ось X
    pygame.draw.line(screen, (0, 0, 0), (center_x, 0), (center_x, HEIGHT), 2)  # Ось Y

def draw_circle_equation(screen, center_x, center_y, radius, scale, offset_x, offset_y):
    radius = int(radius * 20)
    global flag
    """Рисует окружность, вычисляя координаты на основе уравнения окружности."""

    previous_y = None  # Переменная для хранения предыдущего y для верхней части
    for x in range(-radius, radius + 1):
        # Вычисляем y по формуле y = sqrt(R^2 - x^2)
        y = int(round(math.sqrt(radius ** 2 - x ** 2)))

        # Корректируем координаты с учетом PIXEL_SIZE
        pixel_x = (center_x + x) * PIXEL_SIZE * scale + offset_x
        pixel_y_upper = (center_y + y) * PIXEL_SIZE * scale + offset_y
        pixel_y_lower = (center_y - y) * PIXEL_SIZE * scale + offset_y

        # Отрисовка симметричных точек
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pixel_x, pixel_y_upper, PIXEL_SIZE * scale, PIXEL_SIZE * scale))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pixel_x, pixel_y_lower, PIXEL_SIZE * scale, PIXEL_SIZE * scale))
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect((center_x - x) * PIXEL_SIZE * scale + offset_x, pixel_y_upper, PIXEL_SIZE * scale,
                                     PIXEL_SIZE * scale))
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect((center_x - x) * PIXEL_SIZE * scale + offset_x, pixel_y_lower, PIXEL_SIZE * scale,
                                     PIXEL_SIZE * scale))

        # Если это не первая итерация, проверяем промежуточные точки для верхней части
        if previous_y is not None and abs(previous_y - y) > 1:
            # Находим промежуточные точки между предыдущим y и текущим y
            for intermediate_y in range(previous_y + 1, y):  # добавляем только для верхней части
                # Рисуем промежуточные точки на том же x
                intermediate_y_pixel_upper = (center_y + intermediate_y) * PIXEL_SIZE * scale + offset_y
                intermediate_y_pixel_lower = (center_y - intermediate_y) * PIXEL_SIZE * scale + offset_y
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(pixel_x - 1 * PIXEL_SIZE * scale, intermediate_y_pixel_upper,
                                             PIXEL_SIZE * scale, PIXEL_SIZE * scale))
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(pixel_x - 1 * PIXEL_SIZE * scale, intermediate_y_pixel_lower,
                                             PIXEL_SIZE * scale, PIXEL_SIZE * scale))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((center_x - previous_x) * PIXEL_SIZE * scale + offset_x,
                                                                intermediate_y_pixel_upper, PIXEL_SIZE * scale,
                                                                PIXEL_SIZE * scale))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((center_x - previous_x) * PIXEL_SIZE * scale + offset_x,
                                                                intermediate_y_pixel_lower, PIXEL_SIZE * scale,
                                                                PIXEL_SIZE * scale))

        previous_y = y  # Сохраняем текущее y как предыдущее для следующей итерации
        previous_x = x

        if flag:
            pygame.display.flip()
            pygame.time.delay(DELAY_MS)

    flag = False

def algorithm_B_round(pixel_map, center, radius, outline_color):
    # Алгоритм растеризации окружности (дуги) «Б» для рисования контура
    for angle in range(0, 360):  # Изменение угла от 0 до 360 градусов
        rad = math.radians(angle)  # Преобразование градусов в радианы
        x = int(center[0] + radius * math.cos(rad))
        y = int(center[1] + radius * math.sin(rad))

        # Проверяем, не выходит ли точка за границы карты пикселей
        if 0 <= x < len(pixel_map[0]) and 0 <= y < len(pixel_map):
            pixel_map[y][x] = outline_color  # Используем цвет контура
            yield  # Возвращаем управление, чтобы сделать задержку
            pygame.time.delay(DELAY_MS)  # Задержка между точками


def algorithm_B_fill(pixel_map, center, radius, fill_color, outline_color):
    # Затравка (заливка) круговой области
    y = 0
    while y <= radius:
        # Вычисляем x по формуле окружности
        x = int(math.sqrt(radius ** 2 - y ** 2))

        # Заполняем пиксели в пределах окружности для данной строки
        for fill_x in range(center[0] - x, center[0] + x + 1):
            if 0 <= fill_x < len(pixel_map[0]) and 0 <= center[1] + y < len(pixel_map):
                if pixel_map[center[1] + y][fill_x] != outline_color:  # Проверка, не перекрашиваем ли контур
                    pixel_map[center[1] + y][fill_x] = fill_color  # Используем цвет заливки
            if 0 <= fill_x < len(pixel_map[0]) and 0 <= center[1] - y < len(pixel_map):
                if pixel_map[center[1] - y][fill_x] != outline_color:  # Проверка, не перекрашиваем ли контур
                    pixel_map[center[1] - y][fill_x] = fill_color  # Используем цвет заливки

        yield  # Возвращаем управление, чтобы сделать задержку
        pygame.time.delay(DELAY_MS*100)  # Задержка между строками
        y += 1


def create_example_pattern(pixel_map, outline_color, fill_color):
    center_x = len(pixel_map[0]) // 2
    center_y = len(pixel_map) // 2
    radius = 50

    # 1
    # Возвращаем генераторы для отрисовки контура окружности и заливки
    outline_drawing = algorithm_B_round(pixel_map, (center_x, center_y), radius, outline_color)
    fill_drawing = algorithm_B_fill(pixel_map, (center_x, center_y), radius, fill_color, outline_color)

    return outline_drawing, fill_drawing, (center_x, center_y, radius)  # Возвращаем генераторы и параметры


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Canvas")

    scale = INITIAL_SCALE
    offset_x, offset_y = 0, 0
    dragging = False
    last_mouse_x, last_mouse_y = 0, 0

    # Инициализируем карту пикселей
    pixel_map = [[None for _ in range(WIDTH // PIXEL_SIZE)] for _ in range(HEIGHT // PIXEL_SIZE)]

    # Пример с разными цветами для контура и заливки
    outline_color = (255, 0, 0)  # Красный цвет для контура
    fill_color = (0, 0, 255)      # Синий цвет для заливки

    # Создаем генераторы для отрисовки контура окружности и заливки
    circle_drawing, fill_drawing, circle_params = create_example_pattern(pixel_map, outline_color, fill_color)
    circle_center, radius = circle_params[0:2], circle_params[2]

    circle_drawn = False  # Флаг для отслеживания завершения отрисовки круга
    filling = False  # Флаг для отслеживания выполнения затравки
    filling_generator = None  # Генератор для затравки

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Управление масштабированием с помощью колесика мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Правая кнопка мыши
                    dragging = True
                    last_mouse_x, last_mouse_y = event.pos  # Сохраняем начальную позицию
                elif event.button == 4:  # Колесо мыши (прокрутка вверх)
                    # Увеличиваем масштаб с фокусировкой на центр координат
                    new_scale = min(scale + 0.1, MAX_SCALE)
                    offset_x -= (WIDTH // 2 - offset_x) * (new_scale / scale - 1)
                    offset_y -= (HEIGHT // 2 - offset_y) * (new_scale / scale - 1)
                    scale = new_scale
                elif event.button == 5:  # Колесо мыши (прокрутка вниз)
                    # Уменьшаем масштаб с фокусировкой на центр координат
                    new_scale = max(scale - 0.1, MIN_SCALE)
                    offset_x -= (WIDTH // 2 - offset_x) * (new_scale / scale - 1)
                    offset_y -= (HEIGHT // 2 - offset_y) * (new_scale / scale - 1)
                    scale = new_scale

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:  # Правая кнопка мыши
                    dragging = False

            # Перемещение холста при перетаскивании
            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                offset_x += mouse_x - last_mouse_x
                offset_y += mouse_y - last_mouse_y
                last_mouse_x, last_mouse_y = mouse_x, mouse_y

        # Если есть еще пиксели для отрисовки, отрисовываем их
        if not circle_drawn:
            try:
                next(circle_drawing)
            except StopIteration:
                circle_drawn = True  # Устанавливаем флаг, когда отрисовка завершена

        if circle_drawn and not filling:
            filling = True
            filling_generator = fill_drawing  # Запускаем затравку

        # Выполняем затравку с задержкой
        if filling:
            try:
                next(filling_generator)
            except StopIteration:
                filling = False  # Завершаем затравку

        draw_canvas(screen, scale, pixel_map, offset_x, offset_y)
        draw_circle_equation(screen, (WIDTH // PIXEL_SIZE) // 2, (HEIGHT // PIXEL_SIZE) // 2, 1.15, scale, offset_x,
                             offset_y)
        pygame.display.flip()

        # Задержка для замедления отрисовки
        pygame.time.delay(DELAY_MS)


if __name__ == "__main__":
    main()
