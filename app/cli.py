import click
import os
from app.parser import parse_k_file
from app.processor import filter_elements_by_subregion, group_nodes_by_coordinate, find_elements_for_layer


@click.command()
@click.option("--input", default="data/input", help="Папка с исходными файлами")
@click.option("--subregion", default=1, type=int, help="Подобласть для фильтрации")
@click.option("--coordinate", default='Y', type=str, help="Координата для фильтрации слоев")
@click.option("--output", default="data/output", help="Папка для сохранения")
def run(input, subregion, coordinate, output):
    k_file_path = os.path.join(input, "test0.k")  # Формируем путь к файлу

    print("Чтение файла:", k_file_path)
    nodes, elements = parse_k_file(k_file_path)

    print(f"Фильтрация элементов по подобласти {subregion}...")
    filtered_elements = filter_elements_by_subregion(elements, subregion)

    print("Узлы:", nodes)
    print("Отфильтрованные элементы:", filtered_elements)

    print("Фильтрация выполнена\n")

    print(f"Отберем id слов по порядку от 0 по координате {coordinate}\n")
    group_nodes = group_nodes_by_coordinate(nodes, coordinate)
    for coord_value, id in group_nodes.items():
        print(f"SID: {coordinate} = {coord_value}:")
        print("ID:")
        for element_id in id:
            print(f"      - {element_id}")
        print()

    print(f"Отбираем элементы, которые принадлежат слою по координате {coordinate}\n")
    layer_elements = find_elements_for_layer(nodes, filtered_elements, coordinate)
    for coord_value, elements_in_layer in layer_elements.items():
        print(f"SID: {coordinate} = {coord_value}:")
        print("ELEMENTS:")
        for element_id in elements_in_layer:
            print(f"      - {element_id}")
        print()

    print("Выполнено\n")


if __name__ == "__main__":
    run()
