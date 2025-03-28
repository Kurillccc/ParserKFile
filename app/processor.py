from typing import Dict, Tuple, List


def filter_elements_by_subregion(elements: Dict[int, Dict[str, List[int]]], target_subregion: int) -> Dict[
    int, List[int]]:
    """Фильтрует элементы, оставляя только те, что принадлежат заданной подобласти."""
    return {
        element_id: data["nodes"]
        for element_id, data in elements.items()
        if data["subregion"] == target_subregion
    }


def group_nodes_by_coordinate(nodes: Dict[int, Tuple[float, float, float]], coordinate: str) -> Dict[float, List[int]]:
    """Группирует узлы по координате X, Y или Z."""
    grouped_nodes: Dict[float, List[int]] = {}

    for node_id, (x, y, z) in nodes.items():
        if coordinate == "X":
            coord_value = x
        elif coordinate == "Y":
            coord_value = y
        elif coordinate == "Z":
            coord_value = z
        else:
            raise ValueError("Некорректная координата. Используйте 'X', 'Y' или 'Z'.")

        if coord_value not in grouped_nodes:
            grouped_nodes[coord_value] = []

        grouped_nodes[coord_value].append(node_id)

    return grouped_nodes


def find_elements_for_layer(
        nodes: Dict[int, Tuple[float, float, float]],
        elements: Dict[int, List[int]],
        coordinate: str
) -> Dict[float, List[int]]:
    """Для каждого слоя находит элементы, связанные с узлами этого слоя."""
    grouped_nodes = group_nodes_by_coordinate(nodes, coordinate)

    layer_elements: Dict[float, List[int]] = {}
    processed_elements = set()  # Множество для отслеживания уже обработанных элементов

    for coord_value, node_ids in grouped_nodes.items():
        elements_in_layer = []

        for element_id, node_ids_in_element in elements.items():
            if element_id not in processed_elements and any(node_id in node_ids for node_id in node_ids_in_element):
                elements_in_layer.append(element_id)
                processed_elements.add(element_id)  # Добавляем элемент в множество обработанных

        # Если в слое есть элементы, добавляем их в словарь
        layer_elements[coord_value] = elements_in_layer

    # Проверка на одинаковое количество элементов в каждом слое
    element_counts = [len(elements) for elements in layer_elements.values() if elements]  # исключили пустые слои
    if len(set(element_counts)) > 1:
        raise ValueError("Ошибка: количество элементов в слоях не совпадает!")

    # Удаление последнего слоя, если он пустой
    if layer_elements and not layer_elements[list(layer_elements.keys())[-1]]:
        del layer_elements[list(layer_elements.keys())[-1]]

    return layer_elements
