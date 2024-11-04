from RasterImageFile import RasterImageFile
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class RasterImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raster Image Viewer")

        self.image_file = None
        self.scale_factor = 100  # Масштаб изображения в процентах
        self.offset_x = 0  # Смещение по горизонтали
        self.offset_y = 0  # Смещение по вертикали
        self.show_grid = False  # Флаг для отображения сетки

        # Интерфейс выбора файла
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5)

        # Поля для ввода масштаба и смещения
        self.scale_label = tk.Label(root, text="Scale (%):")
        self.scale_label.pack()
        self.scale_entry = tk.Entry(root)
        self.scale_entry.insert(0, "300")
        self.scale_entry.pack()

        self.offset_x_label = tk.Label(root, text="Offset X (px):")
        self.offset_x_label.pack()
        self.offset_x_entry = tk.Entry(root)
        self.offset_x_entry.insert(0, "0")
        self.offset_x_entry.pack()

        self.offset_y_label = tk.Label(root, text="Offset Y (px):")
        self.offset_y_label.pack()
        self.offset_y_entry = tk.Entry(root)
        self.offset_y_entry.insert(0, "0")
        self.offset_y_entry.pack()

        # Чекбокс для включения/отключения сетки
        self.grid_check = tk.Checkbutton(root, text="Show Grid", command=self.toggle_grid)
        self.grid_check.pack()

        # Кнопка для применения настроек
        self.apply_button = tk.Button(root, text="Apply", command=self.apply_settings)
        self.apply_button.pack(pady=5)

        # Метка для отображения информации
        self.info_label = tk.Label(root, text="")
        self.info_label.pack(pady=5)

        # Область для отображения изображения
        self.canvas = tk.Canvas(root, width=400, height=400, bg="gray")
        self.canvas.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select a raster image file",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.image_file = RasterImageFile(file_path)
                self.image_file.read()  # Чтение данных из файла
                self.display_info()  # Отображение информации об изображении
                self.apply_settings()  # Применение настроек отображения
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def display_info(self):
        # Вывод информации о файле
        info = (
            f"{self.image_file.file_path}\n"
            f"{self.image_file.width} {self.image_file.height} {self.image_file.bpp} {self.image_file.palette_rows}x{self.image_file.palette_columns}\n"
        )

        self.info_label.config(text=info)

    def apply_settings(self):
        try:
            # Получаем масштаб и смещения от пользователя
            self.scale_factor = int(self.scale_entry.get())
            self.offset_x = int(self.offset_x_entry.get())
            self.offset_y = int(self.offset_y_entry.get())
            self.display_image()  # Отображение изображения с новыми настройками
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

    def toggle_grid(self):
        # Переключаем флаг отображения сетки
        self.show_grid = not self.show_grid
        self.display_image()

    def display_image(self):
        # Получаем изображение из класса RasterImageFile
        image = self.image_file.get_image()

        # Масштабируем изображение с учетом scale_factor
        scale = self.scale_factor / 100
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        enlarged_image = image.resize((new_width, new_height), Image.NEAREST)

        # Устанавливаем размеры canvas под размер увеличенного изображения
        self.canvas.config(width=new_width, height=new_height)

        # Отображаем увеличенное изображение на canvas с учетом смещения
        self.image_tk = ImageTk.PhotoImage(enlarged_image)
        self.canvas.create_image(self.offset_x, self.offset_y, image=self.image_tk, anchor=tk.NW)

        # Если включен режим отображения сетки, рисуем сетку
        if self.show_grid and scale >= 2:
            self.draw_grid(new_width, new_height, int(1 * scale))

    def draw_grid(self, width, height, cell_size):
        # Очищаем canvas перед рисованием сетки
        self.canvas.delete("grid_line")  # Удаляем предыдущие линии сетки

        # Рисуем сетку на canvas
        for x in range(0, width, cell_size):
            self.canvas.create_line(x, 0, x, height, fill="black", width=1, tags="grid_line")
        for y in range(0, height, cell_size):
            self.canvas.create_line(0, y, width, y, fill="black", width=1, tags="grid_line")

if __name__ == "__main__":
    root = tk.Tk()
    app = RasterImageApp(root)
    root.mainloop()
