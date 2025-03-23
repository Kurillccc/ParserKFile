import uuid
import yaml
import os

from app.processor import find_elements_for_layer

def generate_unique_id():
    """Генерация уникального идентификатора."""
    return uuid.uuid4().hex


def generate_layer_data(num_layers, coordinate, density, h, nodes, filtered_elements):
    """Генерация данных для всех слоев с учетом выбранной координаты."""
    cell_sets = []
    initial_stress_set = []
    set_solid = []

    layer_elements = find_elements_for_layer(nodes, filtered_elements, coordinate)

    for i, (coord_value, elements_in_layer) in enumerate(layer_elements.items()):
        layer_id = i + 1
        unic_id = generate_unique_id()
        new_unic_id = generate_unique_id()

        # Вычисление высоты слоя (h_for_layer)
        h_for_layer = h * (num_layers - layer_id) / (num_layers - 1) if num_layers > 1 else h

        # Определяем значения SIG в зависимости от выбранной координаты
        sigxx = density * 9.8 * h_for_layer if coordinate == 'X' else 0
        sigyy = density * 9.8 * h_for_layer if coordinate == 'Y' else 0
        sigzz = density * 9.8 * h_for_layer if coordinate == 'Z' else 0

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


def write_to_yaml(data, file_path):
    """Запись данных в YAML файл."""
    directory = os.path.dirname(file_path)

    # Создаем путь для нового файла (например, output.yaml)
    output_file_path = os.path.join(directory, 'output.k')

    # Запись в YAML
    with open(output_file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return directory