import os
import uuid
from typing import Dict, List, Any

import yaml

from app.processor import find_elements_for_layer
from app.settings import input_file_name, output_file_name, BASE_DIR


class CustomDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, False)


def generate_unique_id() -> str:
    """Генерация уникального идентификатора."""
    return uuid.uuid4().hex


def generate_layer_data(num_layers: int, coordinate: str, density: float, PR: float, h: float,
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
        if coordinate == 'X':
            sigxx: float = density * 9.8 * h_for_layer
            sigyy: float = density * PR / (1 - PR)
            sigzz: float = density * PR / (1 - PR)
        elif coordinate == 'Y':
            sigxx: float = density * PR / (1 - PR)
            sigyy: float = density * 9.8 * h_for_layer
            sigzz: float = density * PR / (1 - PR)
        elif coordinate == 'Z':
            sigxx: float = density * PR / (1 - PR)
            sigyy: float = density * PR / (1 - PR)
            sigzz: float = density * 9.8 * h_for_layer

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


def write_to_yaml(data: Dict[str, Any], file_path: str, output_path: str) -> str:
    """Запись данных в YAML файл."""
    directory: str = os.path.dirname(file_path)

    # Создаем путь для нового файла (например, output.yaml)
    output_file_path: str = os.path.join(BASE_DIR, "data", "output", f"{output_file_name}_data.k")

    # Запись в YAML
    with open(output_file_path, 'w', encoding="utf-8") as file:
        yaml.dump(data, file, Dumper=CustomDumper, default_flow_style=False, allow_unicode=True, sort_keys=False,
                  indent=2)

    return directory


def write_to_cd_by_k_word(data: Dict[str, Any], section_name: str, file_path_cd: str, output_path: str,
                          key_word: str) -> None:
    if not ".cd" in file_path_cd:
        if not "output" in file_path_cd:
            file_path_cd += "/" + input_file_name + ".cd"
        else:
            file_path_cd: str = os.path.join(BASE_DIR, "data", "output", f"{output_file_name}.cd")
    file_path_txt: str = file_path_cd + ".txt"
    os.rename(file_path_cd, file_path_txt)
    output_lines = []
    last_line: bool = False
    try:
        with open(file_path_txt, "r", encoding="utf-8") as file:
            lines = file.readlines()

        inserting: bool = False  # Флаг, показывающий, когда нужно вставлять данные
        found_key_word: bool = False  # Флаг, показывающий, что нашли строку "1"

        for i, line in enumerate(lines):
            if found_key_word and not inserting:
                if line.startswith((" ", "\t")) and i != len(lines) - 1:
                    output_lines.append(line)
                    continue  # Пропускаем строки с пробелами
                else:
                    if i == len(lines) - 1:
                        output_lines.append(line)
                        last_line = True
                    # Нашли следующую секцию, вставляем данные перед ней
                    output_lines.append(
                        yaml.dump({section_name: data[section_name]}, Dumper=CustomDumper, default_flow_style=False,
                                  allow_unicode=True, sort_keys=False,
                                  indent=2))
                    inserting = True  # Устанавливаем флаг, чтобы вставка произошла только один раз

            if line.strip() == key_word:
                found_key_word = True

            if not last_line: output_lines.append(line)
    except Exception as e:
        print(f"Не удалось вставить данные в cd файл\nОшибка{e}")
    finally:
        # Возвращаем обратно в .cd
        os.rename(file_path_txt, file_path_cd)

    output_file_path: str = os.path.join(BASE_DIR, "data", "output", f"{output_file_name}.cd")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(output_lines)
