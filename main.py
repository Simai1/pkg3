import pygame
import sys
import math
from config import *
from algorithms import *

def draw_canvas(screen, scale, pixel_map, offset_x, offset_y):
    # Заливаем экран белым цветом
    screen.fill((230, 230, 230))
    # Рисуем рамки для каждого пикселя
    for y in range(0, HEIGHT // PIXEL_SIZE):
        for x in range(0, WIDTH // PIXEL_SIZE):
            # Увеличиваем размер пикселя по масштабу
            rect = pygame.Rect((x * PIXEL_SIZE * scale) + offset_x, (y * PIXEL_SIZE * scale) + offset_y,
                               PIXEL_SIZE * scale, PIXEL_SIZE * scale)
            if scale >= 3:
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

    # Рисуем засечки на каждой 20-й ячейке
    tick_length = 7 * scale  # Увеличенная длина засечки для лучшей видимости
    tick_thickness = 2  # Толщина засечки
    for i in range(0, WIDTH // PIXEL_SIZE, 20):
        # Засечки по оси X
        tick_x = i * PIXEL_SIZE * scale + offset_x
        pygame.draw.line(screen, (0, 0, 0), (tick_x, center_y - tick_length), (tick_x, center_y + tick_length),
                         tick_thickness)

    for i in range(0, HEIGHT // PIXEL_SIZE, 20):
        # Засечки по оси Y
        tick_y = i * PIXEL_SIZE * scale + offset_y
        pygame.draw.line(screen, (0, 0, 0), (center_x - tick_length, tick_y), (center_x + tick_length, tick_y),
                         tick_thickness)


def create_example_pattern(pixel_map, outline_color, fill_color, ):
    center_x = len(pixel_map[0]) // 2 + 40  # 2
    center_y = len(pixel_map) // 2 - 280  # 14
    radius = 23  # 1.15

    # Возвращаем генераторы для отрисовки контура окружности и заливки
    outline_drawing = algorithm_B_round(pixel_map, (center_x, center_y), radius,
                                        outline_color)  # Используем reference_algorithm_round
    fill_drawing = algorithm_reference_fill(pixel_map, (center_x, center_y), radius, fill_color, outline_color)

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
    fill_color = (0, 0, 255)  # Синий цвет для заливки

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
            filling_generator = fill_drawing  # Запускаем затравку2

        # Выполняем затравку с задержкой
        if filling:
            try:
                next(filling_generator)
            except StopIteration:
                filling = False  # Завершаем затравку

        draw_canvas(screen, scale, pixel_map, offset_x, offset_y)
        pygame.display.flip()

        # Задержка для замедления отрисовки
        pygame.time.delay(DELAY_MS)


if __name__ == "__main__":
    main()
