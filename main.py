import tkinter as tk
from tkinter import Scale, HORIZONTAL
from PIL import Image, ImageTk

class PixelArtApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pixel Art with Tkinter and Pillow")

        # Установите начальный размер изображения
        self.size = 50
        self.canvas_size = 800
        self.image = Image.new("RGB", (self.size, self.size), (255, 255, 255))

        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        # Ползунок для изменения размера изображения
        self.scale = Scale(self.master, from_=1, to=100, orient=HORIZONTAL, command=self.update_size)
        self.scale.set(self.size)
        self.scale.pack()

        # Переменные для перемещения
        self.last_x = None
        self.last_y = None

        self.canvas.bind("<Button-1>", self.change_color)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-3>", self.start_move)
        self.canvas.bind("<B3-Motion>", self.move_canvas)

        self.draw_canvas()

    def update_size(self, new_size):
        new_size = int(new_size)
        if new_size != self.size:
            # Создаем новое изображение с новым размером
            new_image = Image.new("RGB", (new_size, new_size), (255, 255, 255))

            # Копируем старые пиксели в новое изображение
            min_size = min(self.size, new_size)
            for x in range(min_size):
                for y in range(min_size):
                    old_color = self.image.getpixel((x, y))
                    new_image.putpixel((x, y), old_color)

            self.image = new_image
            self.size = new_size
            self.draw_canvas()

    def draw_canvas(self):
        self.canvas.delete("all")
        cell_size = self.canvas_size // self.size

        for x in range(self.size):
            for y in range(self.size):
                color = self.image.getpixel((x, y))
                self.canvas.create_rectangle(
                    x * cell_size,
                    y * cell_size,
                    (x + 1) * cell_size,
                    (y + 1) * cell_size,
                    fill=self.rgb_to_hex(color),
                    outline="gray"
                )

    def change_color(self, event):
        cell_size = self.canvas_size // self.size
        x = event.x // cell_size
        y = event.y // cell_size
        # Сменяем цвет пикселя на красный (или выбирайте любой другой цвет)
        self.image.putpixel((x, y), (255, 0, 0))
        self.draw_canvas()

    def paint(self, event):
        cell_size = self.canvas_size // self.size
        x = event.x // cell_size
        y = event.y // cell_size
        self.image.putpixel((x, y), (255, 0, 0))  # Меняем цвет на красный
        self.draw_canvas()

    def start_move(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def move_canvas(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move("all", dx, dy)
        self.last_x = event.x
        self.last_y = event.y

    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()
