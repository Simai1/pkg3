import math
import struct
from PIL import Image

def calculate_bpp(rows, columns):
    bpp_row = math.ceil(math.log2(rows))
    bpp_column = math.ceil(math.log2(columns))
    return bpp_row + bpp_column

class RasterImageFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.width = None
        self.height = None
        self.bpp = None
        self.palette_rows = 5
        self.palette_columns = 3
        self.palette = []
        self.pixels = []

    def write_header(self, width, height):
        self.width = width
        self.height = height
        self.bpp = calculate_bpp(self.palette_rows, self.palette_columns)
        with open(self.file_path, 'wb') as f:
            f.write(struct.pack('H', self.width))
            f.write(struct.pack('H', self.height))
            f.write(struct.pack('B', self.bpp))
            f.write(struct.pack('H', self.palette_rows * self.palette_columns))

    def write_palette(self, palette):
        self.palette = palette
        with open(self.file_path, 'ab') as f:
            for row in self.palette:
                for color in row:
                    f.write(struct.pack('BBBB', *color))  # ARGB

    def write_pixels(self, pixels):
        self.pixels = pixels
        with open(self.file_path, 'ab') as f:
            bit_buffer = 0
            bits_filled = 0
            bpp_row = math.ceil(math.log2(self.palette_rows))
            bpp_column = math.ceil(math.log2(self.palette_columns))

            for row, col in pixels:
                # Упаковываем координаты строки
                bit_buffer = (bit_buffer << bpp_row) | row
                bits_filled += bpp_row

                # Упаковываем координаты столбца
                bit_buffer = (bit_buffer << bpp_column) | col
                bits_filled += bpp_column

                # Записываем, когда буфер заполнен до байта
                while bits_filled >= 8:
                    bits_filled -= 8
                    byte = (bit_buffer >> bits_filled) & 0xFF
                    f.write(struct.pack('B', byte))

            if bits_filled > 0:
                # Вычисляем, сколько битов осталось, и сдвигаем их влево
                byte = bit_buffer << (8 - bits_filled)
                # Оставшиеся биты заполняем в самый младший байт
                byte &= 0xFF  # Убедимся, что записываем только младшие 8 бит
                f.write(struct.pack('B', byte))

    def read_header(self):
        with open(self.file_path, 'rb') as f:
            self.width = struct.unpack('H', f.read(2))[0]
            self.height = struct.unpack('H', f.read(2))[0]
            self.bpp = struct.unpack('B', f.read(1))[0]

    def read_palette(self):
        with open(self.file_path, 'rb') as f:
            f.seek(7)
            self.palette = []
            for _ in range(self.palette_rows):
                row = [struct.unpack('BBBB', f.read(4)) for _ in range(self.palette_columns)]
                self.palette.append(row)


    def read_pixels(self):
        pixel_count = self.width * self.height
        bpp_row = math.ceil(math.log2(self.palette_rows))
        bpp_column = math.ceil(math.log2(self.palette_columns))
        with open(self.file_path, 'rb') as f:
            f.seek(7 + self.palette_rows * self.palette_columns * 4)  # Пропуск заголовка и палитры
            self.pixels = []
            bit_buffer = 0
            bits_remaining = 0

            for _ in range(pixel_count):
                # Читаем байты, пока в буфере недостаточно бит для строки и столбца
                while bits_remaining < bpp_row + bpp_column:
                    byte = struct.unpack('B', f.read(1))[0]
                    bit_buffer = (bit_buffer << 8) | byte
                    bits_remaining += 8

                # Извлекаем координаты строки
                bits_remaining -= bpp_row
                row = (bit_buffer >> bits_remaining) & ((1 << bpp_row) - 1)

                # Извлекаем координаты столбца
                bits_remaining -= bpp_column
                col = (bit_buffer >> bits_remaining) & ((1 << bpp_column) - 1)

                self.pixels.append((row, col))
                bit_buffer &= (1 << bits_remaining) - 1

    def get_image(self):
        image = Image.new("RGBA", (self.width, self.height))  # Изменяем на RGBA
        pixel_data = []

        for row, col in self.pixels:
            if row < self.palette_rows and col < self.palette_columns:
                a, r, g, b = self.palette[row][col]  # Извлекаем альфа и цвет
                pixel_data.append((r, g, b, a))  # Добавляем альфа-канал
            else:
                pixel_data.append((0, 0, 0, 255))  # Черный цвет с полной непрозрачностью

        image.putdata(pixel_data)
        return image

    def display(self):
        # Вывод информации о размере изображения и BPP
        print(f"{self.width} {self.height} {self.bpp} {self.palette_rows}x{self.palette_columns}")

        # Вывод палитры как матрицы
        for row in self.palette:
            print(" ".join([f"ARGB({color[0]}, {color[1]}, {color[2]}, {color[3]})" for color in row]))

        # Вывод пикселей как матрицы
        pixel_matrix = []
        for row, col in self.pixels:
            pixel_matrix.append(f"({row}, {col})")

        print(" ".join(pixel_matrix))

    def read(self):
        self.read_header()
        self.read_palette()
        self.read_pixels()

if __name__ == '__main__':
    # Параметры для теста
    file_path = "../files/pallete.bin"
    width = 3
    height = 5
    palette = [
        [(255, 0, 0, 0), (255, 30, 30, 30), (255, 60, 60, 60)],
        [(255, 255, 0, 0), (255, 255, 60, 30), (255, 255, 120, 120)],
        [(255, 0, 255, 0), (255, 60, 255, 60), (255, 120, 255, 120)],
        [(255, 0, 0, 255), (255, 60, 60, 255), (255, 120, 120, 255)],
        [(255, 0, 255, 255), (255, 60, 255, 255), (255, 120, 255, 255)],
    ]
    pixels = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
        (3, 0), (3, 1), (3, 2),
        (4, 0), (4, 1), (4, 2),
    ]
    print(len(pixels))

    # Создаем объект RasterImageFile
    image = RasterImageFile(file_path)

    # Записываем данные в файл
    image.write_header(width, height)
    image.write_palette(palette)
    image.write_pixels(pixels)

    # Читаем данные из файла
    image.read_header()
    image.read_palette()
    image.read_pixels()

    image.display()