def parse_k_file(file_path):
    """Читает .k-файл и возвращает узлы и элементы."""
    nodes = {}  # Словарь для узлов {номер: (x, y, z)}
    elements = {}  # Словарь для элементов {номер элемента: [номера узлов]}

    with open(file_path, "r") as file:
        lines = file.readlines()

    parsing_nodes = False
    parsing_elements = False

    for line in lines:
        line = line.strip()

        if line.startswith("*NODE"):
            parsing_nodes = True
            parsing_elements = False
            continue

        if line.startswith("*ELEMENT_SOLID"):
            parsing_nodes = False
            parsing_elements = True
            continue

        if line.startswith("*END"):
            parsing_nodes = False
            parsing_elements = False

        if parsing_nodes:
            parts = line.split(",")
            node_id = int(parts[0])  # Номер узла
            x, y, z = map(float, parts[1:4])  # Координаты
            nodes[node_id] = (x, y, z)

        elif parsing_elements:
            parts = line.split(",")
            element_id = int(parts[0])  # Номер КЭ
            subregion = int(parts[1])  # Номер подобласти
            node_ids = list(map(int, parts[2:]))  # Номера узлов входящих в КЭ
            elements[element_id] = {"subregion": subregion, "nodes": node_ids}

    return nodes, elements


def parse_cd_file():
    return 0
