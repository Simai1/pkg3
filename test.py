import pygame
import sys
import math

import RasterImageFile
from config import *
from algorithms import *
from RasterImageFile import RasterImageFile

def arc_length(radius, angle_start, angle_end):
    angle_start = math.radians(angle_start % 360)
    angle_end = math.radians(angle_end % 360)
    if angle_end >= angle_start:
        theta = angle_end - angle_start
    else:
        theta = (2 * math.pi - angle_start) + angle_end
    length = radius * theta
    return length

def draw_canvas(screen, scale, pixel_map, offset_x, offset_y):
    screen.fill((230, 230, 230))
    for y in range(0, HEIGHT // PIXEL_SIZE):
        for x in range(0, WIDTH // PIXEL_SIZE):
            rect = pygame.Rect((x * PIXEL_SIZE * scale) + offset_x, (y * PIXEL_SIZE * scale) + offset_y,
                               PIXEL_SIZE * scale, PIXEL_SIZE * scale)
            if scale >= 3:
                pygame.draw.rect(screen, (192, 192, 192), rect, 1)
            if pixel_map[y][x] is not None:
                pygame.draw.rect(screen, pixel_map[y][x], rect)
    center_x_pixel = (WIDTH // PIXEL_SIZE) // 2
    center_y_pixel = (HEIGHT // PIXEL_SIZE) // 2
    center_x = center_x_pixel * PIXEL_SIZE * scale + offset_x
    center_y = center_y_pixel * PIXEL_SIZE * scale + offset_y
    pygame.draw.line(screen, (0, 0, 0), (0, center_y), (WIDTH, center_y), 2)
    pygame.draw.line(screen, (0, 0, 0), (center_x, 0), (center_x, HEIGHT), 2)
    tick_length = 4 * scale
    tick_thickness = 2
    for i in range(0, WIDTH // PIXEL_SIZE, 20):
        tick_x = i * PIXEL_SIZE * scale + offset_x
        pygame.draw.line(screen, (0, 0, 0), (tick_x, center_y - tick_length), (tick_x, center_y + tick_length),
                         tick_thickness)
    for i in range(0, HEIGHT // PIXEL_SIZE, 20):
        tick_y = i * PIXEL_SIZE * scale + offset_y
        pygame.draw.line(screen, (0, 0, 0), (center_x - tick_length, tick_y), (center_x + tick_length, tick_y),
                         tick_thickness)

def create_example_pattern(pixel_map, outline_color, fill_color, algorithm_round, algorithm_fill, _radius,x,y):
    center_x = len(pixel_map[0]) // 2 + int(x * 20) # 0
    center_y = len(pixel_map) // 2 - int(y * 20)  # 7.4
    radius = int(_radius * 20)  # 3

    # Возвращаем генераторы для отрисовки контура окружности и заливки
    algorithm_round(pixel_map, (center_x, center_y), radius,
                                        outline_color)  # Используем reference_algorithm_round
    algorithm_fill(pixel_map, (center_x, center_y), radius, fill_color, outline_color)

def create_arc_pattern(pixel_map, outline_color, algorithm_round, _radius, x, y, ara, arb):
    center_x = len(pixel_map[0]) // 2 + int(x * 20)
    center_y = len(pixel_map) // 2 - int(y * 20)
    radius = int(_radius * 20)
    algorithm_round(pixel_map, (center_x, center_y), radius, outline_color, ara, arb)

def draw_button(screen, x, y, width, height, text):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (100, 100, 255), button_rect)
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect

def find_index_2d(array, target):
    for row_index, row in enumerate(array):
        if target in row:
            col_index = row.index(target)
            return row_index, col_index
    return None

def create_file(file_path, pixel_map):
    width = WIDTH // PIXEL_SIZE
    height = HEIGHT // PIXEL_SIZE
    pixels = []
    for line in pixel_map:
        for item in line:
            pixels.append(find_index_2d(PALLETE_APP, item))
    image = RasterImageFile(file_path)
    image.write_header(width, height)
    image.write_palette(PALLETE)
    image.write_pixels(pixels)

def read_file(file_path):
    image = RasterImageFile(file_path)
    image.read_header()
    image.read_palette()
    image.read_pixels()
    pixel_map = []
    counter = 0
    for _ in range(HEIGHT // PIXEL_SIZE):
        row = []
        for _ in range(WIDTH // PIXEL_SIZE):
            row.append(PALLETE_APP[image.pixels[counter][0]][image.pixels[counter][1]])
            counter += 1
        pixel_map.append(row)
    return pixel_map

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Canvas")

    for line in PALLETE:
        row = []
        for item in line:
            row.append(item[1:])
        PALLETE_APP.append(row)

    f = True
    scale = INITIAL_SCALE
    offset_x, offset_y = 0, 0
    dragging = False
    last_mouse_x, last_mouse_y = 0, 0
    pixel_map = [[(255, 255, 255) for _ in range(WIDTH // PIXEL_SIZE)] for _ in range(HEIGHT // PIXEL_SIZE)]
    set = draw_button(screen, 20, 20, 100, 50, "set file")
    mkfile = draw_button(screen, 20, 80, 100, 50, "to file")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if set.collidepoint(event.pos):
                        create_file('./files/test.bin', pixel_map)
                    if mkfile.collidepoint(event.pos):
                        pixel_map = read_file('./files/test.bin')
                elif event.button == 3:
                    dragging = True
                    last_mouse_x, last_mouse_y = event.pos
                elif event.button == 4:
                    new_scale = min(scale + 0.1, MAX_SCALE)
                    offset_x -= (WIDTH // 2 - offset_x) * (new_scale / scale - 1)
                    offset_y -= (HEIGHT // 2 - offset_y) * (new_scale / scale - 1)
                    scale = new_scale
                elif event.button == 5:
                    new_scale = max(scale - 0.1, MIN_SCALE)
                    offset_x -= (WIDTH // 2 - offset_x) * (new_scale / scale - 1)
                    offset_y -= (HEIGHT // 2 - offset_y) * (new_scale / scale - 1)
                    scale = new_scale

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                offset_x += mouse_x - last_mouse_x
                offset_y += mouse_y - last_mouse_y
                last_mouse_x, last_mouse_y = mouse_x, mouse_y

        draw_canvas(screen, scale, pixel_map, offset_x, offset_y)
        if (f):
            ar = algorithm_reference_round
            af = algorithm_B_fill
            # create_example_pattern(pixel_map, PALLETE_APP[2][0], PALLETE_APP[2][0], ar, af, 1, 0, 0)
            # create_example_pattern(pixel_map, PALLETE_APP[4][0], PALLETE_APP[4][0], ar, af, 1, 2, 2)
            # create_example_pattern(pixel_map, PALLETE[1][0], PALLETE[1][0], ar, af, 1.15, 2, 12.8)
            # create_example_pattern(pixel_map, PALLETE[2][0], PALLETE[2][0], ar, af, 2, 0, 14)
            # create_example_pattern(pixel_map, PALLETE[3][0], PALLETE[3][0], ar, af, 2, 3, 10.5)
            # create_example_pattern(pixel_map, PALLETE[2][2], PALLETE[2][2], ar, af, 3, 3, 7)
            # create_example_pattern(pixel_map, PALLETE[0][1], PALLETE[0][1], ar, af, 3, 2, 7.1)
            # create_example_pattern(pixel_map, PALLETE[1][1], PALLETE[1][1], ar, af, 3, 0.7, 6.8)
            # create_example_pattern(pixel_map, PALLETE[0][2], PALLETE[0][2], ar, af, 3, 0, 7.4)
            # create_example_pattern(pixel_map, PALLETE[2][1], PALLETE[2][1], ar, af, 1.5, 0.5, 14)
            # create_example_pattern(pixel_map, PALLETE[1][2], PALLETE[1][2], ar, af, 0.2, 1, 14.5)
            f = False


        set = draw_button(screen, 20, 20, 100, 50, "set file")
        mkfile = draw_button(screen, 20, 80, 100, 50, "to file")

        pygame.display.flip()

if __name__ == "__main__":
    main()
