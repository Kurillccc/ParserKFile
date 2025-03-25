import click
import os
import traceback
from typing import Dict, List
from app.parser import parse_k_file
from app.processor import filter_elements_by_subregion, group_nodes_by_coordinate, find_elements_for_layer
from app.generate_yaml import write_to_yaml, generate_layer_data


@click.command()
@click.option("--input", default="data/input", help="Папка с исходными файлами")
@click.option("--subregion", default=1, type=int, help="Подобласть для фильтрации")
@click.option("--coordinate", default='Y', type=str, help="Координата для фильтрации слоев")
@click.option("--density", default=2700.0, type=float, help="Плотность материала (кг/м³)")
@click.option("--h", default=1000.0, type=float, help="Высота слоя (м)")
@click.option("--output", default="data/output", help="Папка для сохранения")
def run(input: str, subregion: int, coordinate: str, density: float, h: float) -> None:
    k_file_path = os.path.join(input, "test0.k")  # Формируем путь к файлу

    print("Чтение файла:", k_file_path)
    try:
        nodes, elements = parse_k_file(k_file_path)
    except Exception as e:
        print(f"Не удалось прочитать файл\nОшибка{e}")

    print(f"Фильтрация элементов по подобласти {subregion}...")
    try:
        filtered_elements = filter_elements_by_subregion(elements, subregion)

        print("Узлы:", nodes)
        print("Отфильтрованные элементы:", filtered_elements)
    except Exception as e:
        print(f"Не удалось отфильтровать элементы по подобласти\nОшибка{e}")

    print(f"Отберем id слов по порядку от 0 по координате {coordinate}\n")
    group_nodes = group_nodes_by_coordinate(nodes, coordinate)
    try:
        for coord_value, id in group_nodes.items():
            print(f"SID: {coordinate} = {coord_value}:")
            print("ID:")
            for element_id in id:
                print(f"      - {element_id}")
            print()
    except Exception as e:
        print(f"Не удалось отобрать id слоев\nОшибка{e}")

    print(f"Отбираем элементы, которые принадлежат слою по координате {coordinate}\n")
    try:
        layer_elements = find_elements_for_layer(nodes, filtered_elements, coordinate)
        for coord_value, elements_in_layer in layer_elements.items():
            print(f"SID: {coordinate} = {coord_value}:")
            print("ELEMENTS:")
            for element_id in elements_in_layer:
                print(f"      - {element_id}")
            print()
    except Exception as e:
        print(f"Не удалось отобрать элементы\nОшибка: {e}")

    print("Переведем файл в требуемый формат")
    try:
        output_file_path = write_to_yaml(
            generate_layer_data(len(layer_elements), coordinate, density, h, nodes, filtered_elements),
            input)
        print(f"Файл сохранен в {output_file_path}")
    except Exception as e:
        print(f"Не удалось создать файл\nОшибка{e}")

    print("Выполнено\n")


if __name__ == "__main__":
    run()
