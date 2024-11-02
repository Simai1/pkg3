import tkinter as tk
from tkinter import Scale, HORIZONTAL
from PIL import Image, ImageTk


class PixelArtApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pixel Art with Tkinter and Pillow")

        # Установите начальный размер изображения
        self.size = 16
        self.canvas_size = 400
        self.image = Image.new("RGB", (self.size, self.size), (255, 255, 255))

        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        # Ползунок для изменения размера изображения
        self.scale = Scale(self.master, from_=1, to=100, orient=HORIZONTAL, command=self.update_size)
        self.scale.set(self.size)
        self.scale.pack()

        self.draw_canvas()

    def update_size(self, new_size):
        self.size = int(new_size)
        self.image = Image.new("RGB", (self.size, self.size), (255, 255, 255))
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

    def rgb_to_hex(self, rgb):
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()
