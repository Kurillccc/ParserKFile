import tkinter as tk
from tkinter import filedialog, messagebox
import os
from app.parser import parse_k_file
from app.processor import filter_elements_by_subregion, find_elements_for_layer, compute_and_generate_output, save_to_file

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Парсинг KFile")
        self.geometry("600x650")

        self.input_file_path = ""
        self.output_folder = "data/output"

        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Кнопка для выбора входного файла
        self.input_button = tk.Button(self, text="Выбрать файл", command=self.select_input_file)
        self.input_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Поле для отображения выбранного файла
        self.input_file_label = tk.Label(self, text="Выберите файл для обработки")
        self.input_file_label.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Ввод для подобласти
        self.subregion_label = tk.Label(self, text="Введите номер подобласти:")
        self.subregion_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        # Текстовое поле для ввода номера подобласти
        self.subregion_entry = tk.Entry(self)
        self.subregion_entry.grid(row=1, column=1, pady=5, padx=10)

        # Ввод для высоты
        self.h_label = tk.Label(self, text="Введите h:")
        self.h_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        # Текстовое поле для ввода высоты
        self.h_entry = tk.Entry(self)
        self.h_entry.grid(row=2, column=1, pady=5, padx=10)

        # Ввод для числа слоев
        self.layer_label = tk.Label(self, text="Введите число слоев:")
        self.layer_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        # Текстовое поле для ввода числа слоев
        self.layer_entry = tk.Entry(self)
        self.layer_entry.grid(row=3, column=1, pady=5, padx=10)

        # Ввод для плотности
        self.density_label = tk.Label(self, text="Введите плотность:")
        self.density_label.grid(row=4, column=0, pady=5, padx=10, sticky="w")

        # Текстовое поле для ввода плотности
        self.density_entry = tk.Entry(self)
        self.density_entry.grid(row=4, column=1, pady=5, padx=10)

        # Выпадающий список для выбора координаты (X, Y, Z)
        self.coordinate_label = tk.Label(self, text="Выберите координату (X, Y, Z):")
        self.coordinate_label.grid(row=5, column=0, pady=5, padx=10, sticky="w")

        self.coordinate_option = tk.OptionMenu(self, tk.StringVar(), *["X", "Y", "Z"])
        self.coordinate_option.grid(row=5, column=1, pady=5, padx=10)

        # Кнопка для обработки данных
        self.process_button = tk.Button(self, text="Обработать", command=self.process_data)
        self.process_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Текстовое поле для отображения результатов
        self.output_text = tk.Text(self, height=25, width=84)
        self.output_text.grid(row=7, column=0, columnspan=2, pady=10)

    def select_input_file(self):
        """Открывает диалог для выбора файла"""
        self.input_file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Text files", "*.k")])
        if self.input_file_path:
            self.input_file_label.config(text=os.path.basename(self.input_file_path))

    def process_data(self):
        """Обрабатывает данные при нажатии кнопки"""
        if not self.input_file_path:
            messagebox.showerror("Ошибка", "Выберите файл для обработки")
            return

        subregion = int(self.subregion_option.get())
        h = int(self.h.get())
        layer_count = int(self.layer_count.get())
        density = int(self.density.get())
        coordinate = self.coordinate_option.get()

        try:
            # Парсим файл
            nodes, elements = parse_k_file(self.input_file_path, subregion)

            # Фильтруем элементы
            filtered_elements = filter_elements_by_subregion(elements, subregion)

            # Находим элементы по слоям
            layer_elements = find_elements_for_layer(nodes, filtered_elements, coordinate)

            # Формируем и выводим данные
            output_data = compute_and_generate_output(nodes, filtered_elements)
            output_file_path = os.path.join(self.output_folder, f"output_{coordinate}.txt")
            save_to_file(output_data, output_file_path)

            # Отображаем результаты в текстовом поле
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Результаты сохранены в {output_file_path}\n")
            self.output_text.insert(tk.END, "\n".join(output_data))

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обработке данных: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
