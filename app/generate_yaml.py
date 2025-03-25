import uuid
import yaml
import os

from typing import Dict, List, Any
from app.processor import find_elements_for_layer


class CustomDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)


def generate_unique_id() -> str:
    """Генерация уникального идентификатора."""
    return uuid.uuid4().hex


def generate_layer_data(num_layers: int, coordinate: str, density: float, h: float,
                        nodes: Dict[int, List[float]], filtered_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Генерация данных для всех слоев с учетом выбранной координаты."""
    cell_sets: List[Dict[str, Any]] = []
    initial_stress_set: List[Dict[str, Any]] = []
    set_solid: List[Dict[str, Any]] = []

    layer_elements: Dict[float, List[int]] = find_elements_for_layer(nodes, filtered_elements, coordinate)

    for i, (coord_value, elements_in_layer) in enumerate(layer_elements.items()):
        layer_id: int = i + 1
        unic_id: str = generate_unique_id()
        new_unic_id: str = generate_unique_id()

        # Вычисление высоты слоя (h_for_layer)
        h_for_layer: float = h * (num_layers - layer_id) / (num_layers - 1) if num_layers > 1 else h

        # Определяем значения SIG в зависимости от выбранной координаты
        sigxx: float = density * 9.8 * h_for_layer if coordinate == 'X' else 0
        sigyy: float = density * 9.8 * h_for_layer if coordinate == 'Y' else 0
        sigzz: float = density * 9.8 * h_for_layer if coordinate == 'Z' else 0

        # Заполнение данных для CELL_SETS
        cell_sets.append({
            'Id': layer_id,
            'Name': f'set{layer_id}',
            'Count': len(elements_in_layer),
            '_ref_used_': 1,
            'uid': unic_id,
            'parentUid': '',
            '__excludeRun__': '~'
        })

        # Заполнение данных для INITIAL_STRESS_SET
        initial_stress_set.append({
            'ESID': layer_id,
            'SIGXX': sigxx,
            'SIGYY': sigyy,
            'SIGZZ': sigzz,
            'SIGXY': 0,
            'SIGYZ': 0,
            'SIGZX': 0,
            'EPS': 0,
            'name': f'set{layer_id}',
            'uid': new_unic_id,
            'parentUid': '',
            '__excludeRun__': '~'
        })

        # Заполнение данных для SET_SOLID
        set_solid.append({
            'NAME': f'set{layer_id}',
            'SID': layer_id,
            'ELEMENTS': elements_in_layer  # Список элементов для этого слоя
        })

    return {
        'CELL_SETS': cell_sets,
        'INITIAL_STRESS_SET': initial_stress_set,
        'SET_SOLID': set_solid
    }


def write_to_yaml(data: Dict[str, Any], file_path: str) -> str:
    """Запись данных в YAML файл."""
    directory: str = os.path.dirname(file_path)

    # Создаем путь для нового файла (например, output.yaml)
    output_file_path: str = os.path.join(directory, 'output.k')

    # Запись в YAML
    with open(output_file_path, 'w') as file:
        yaml.dump(data, file, Dumper=CustomDumper, default_flow_style=False, allow_unicode=True, sort_keys=False,
                  indent=2)

    return directory
