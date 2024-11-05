import pygame
import sys
import math
from config import *
from algorithms import *

def arc_length(radius, angle_start, angle_end):
    # Преобразуем углы из градусов в радианы
    angle_start = math.radians(angle_start % 360)
    angle_end = math.radians(angle_end % 360)

    # Рассчитываем угловую разницу в радианах
    if angle_end >= angle_start:
        theta = angle_end - angle_start
    else:
        theta = (2 * math.pi - angle_start) + angle_end

    # Вычисляем длину дуги
    length = radius * theta
    return length


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
    tick_length = 4 * scale  # Увеличенная длина засечки для лучшей видимости
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


def create_example_pattern(pixel_map, outline_color, fill_color, algorithm_round, algorithm_fill, _radius, x, y):
    center_x = len(pixel_map[0]) // 2 + int(x * 20)
    center_y = len(pixel_map) // 2 - int(y * 20)
    radius = int(_radius * 20)

    # Возвращаем генераторы для отрисовки контура окружности и заливки
    algorithm_round(pixel_map, (center_x, center_y), radius,
                    outline_color)  # Используем reference_algorithm_round
    # algorithm_fill(pixel_map, (center_x, center_y), radius, fill_color, outline_color)


def create_arc_pattern(pixel_map, outline_color, algorithm_round, _radius, x, y, ara, arb):
    # print(f"Длина дуги: {arc_length(_radius, ara, arb)}")
    center_x = len(pixel_map[0]) // 2 + int(x * 20)
    center_y = len(pixel_map) // 2 - int(y * 20)
    radius = int(_radius * 20)  # 3
    algorithm_round(pixel_map, (center_x, center_y), radius, outline_color, ara, arb)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Canvas")

    f = True
    scale = INITIAL_SCALE
    offset_x, offset_y = 0, 0
    dragging = False
    last_mouse_x, last_mouse_y = 0, 0

    # Инициализируем карту пикселей
    pixel_map = [[None for _ in range(WIDTH // PIXEL_SIZE)] for _ in range(HEIGHT // PIXEL_SIZE)]

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

        draw_canvas(screen, scale, pixel_map, offset_x, offset_y)
        if (f):
            # ar = algorithm_reference_round
            # af = algorithm_A_fill
            ar1, ar2, ar3 = algorithm_reference_round, algorithm_A_round, algorithm_B_round
            ara, arb = 0, 360

            create_arc_pattern(pixel_map, (255, 0, 0), ar2, 1, 0, 0, ara, arb)
            create_arc_pattern(pixel_map, (255, 0, 0), ar1, 1, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 3, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 4, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 5, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 6, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 7, 0, 0, ara, arb)

            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 1, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 2, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 3, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 4, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 5, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 6, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar2, 7, 0, 0, ara, arb)

            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 1, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 2, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 3, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 4, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 5, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 6, 0, 0, ara, arb)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 7, 0, 0, ara, arb)

            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 2, 0, 0, 0, 180)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 3, 0, 0, 0, 180)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 4, 0, 0, 0, 180)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 5, 0, 0, 0, 180)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 6, 0, 0, 0, 180)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar1, 7, 0, 0, 0, 180)


            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 10, 0, 0, 0, 180)
            # create_arc_pattern(pixel_map, (255, 140, 0), ar3, 5, 0, 0, 0, 270)
            # create_example_pattern(pixel_map, (255, 140, 0), (255, 141, 0), ar, af, 3, 0, 0)
            # create_example_pattern(pixel_map, (255, 140, 0), (255, 141, 0), ar, af, 1, 2, 14)  # Окружность 1
            # create_example_pattern(pixel_map, (255, 255, 255), (255, 255, 255), ar, af, 1.15, 2, 12.8)  # Окружность 2
            # create_example_pattern(pixel_map, (255, 140, 0), (255, 140, 0), ar, af, 2, 0, 14)  # Окружность 3
            # create_example_pattern(pixel_map, (255, 140, 0), (255, 140, 0), ar, af, 2, 3, 10.5)  # Окружность 4
            # create_example_pattern(pixel_map, (255, 140, 0), (255, 140, 0), ar, af, 1.5, -1, 10)  # Окружность 5
            # create_example_pattern(pixel_map, (0, 255, 0), (0, 255, 0), ar, af, 3, 3, 7)  # Окружность 6
            # create_example_pattern(pixel_map, (255, 255, 255), (255, 255, 255), ar, af, 3, 1.5, 6.6)  # Окружность 7
            # create_example_pattern(pixel_map, (255, 255, 0), (255, 255, 0), ar, af, 3, 2, 7.1)  # Окружность 8
            # create_example_pattern(pixel_map, (255, 255, 255), (255, 255, 255), ar, af, 3, 0.7, 6.8)  # Окружность 9
            # create_example_pattern(pixel_map, (0, 0, 255), (0, 0, 255), ar, af, 3, 1.3, 7.5)  # Окружность 10
            # create_example_pattern(pixel_map, (255, 255, 255), (255, 255, 255), ar, af, 3, 0, 7.4)  # Окружность 11
            # create_example_pattern(pixel_map, (255, 255, 0), (255, 255, 0), ar, af, 1.5, 0.5, 14)  # Окружность 12
            # create_example_pattern(pixel_map, (0, 0, 0), (0, 0, 0), ar, af, 0.2, 1, 14.5)  # Окружность 13
            f = False

        pygame.display.flip()

        # Задержка для замедления отрисовки
        # pygame.time.delay(DELAY_MS)


if __name__ == "__main__":
    main()
