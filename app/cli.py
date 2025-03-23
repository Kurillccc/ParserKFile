import click
import os
from app.parser import parse_k_file
from app.processor import filter_elements_by_subregion


@click.command()
@click.option("--input", default="data/input", help="Папка с исходными файлами")
@click.option("--subregion", default=1, type=int, help="Подобласть для фильтрации")
@click.option("--output", default="data/output", help="Папка для сохранения")
def run(input, subregion, output):
    k_file_path = os.path.join(input, "test0.k")  # Формируем путь к файлу

    print("Чтение файла:", k_file_path)
    nodes, elements = parse_k_file(k_file_path)

    print(f"Фильтрация элементов по подобласти {subregion}...")
    filtered_elements = filter_elements_by_subregion(elements, subregion)  # Фильтруем

    print("Узлы:", nodes)
    print("Отфильтрованные элементы:", filtered_elements)

    print("Выполнено")


if __name__ == "__main__":
    run()
