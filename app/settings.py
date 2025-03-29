import os

# Навзвание входных файлов
input_file_name: str = "test0"
# Название выходных файлов
output_file_name: str = "test2"

# После MESH_PARTS: вставится cell_sets
put_cell_sets: str = "MESH_PARTS:"
# После COMMON_SETTINGS: вставится stress_set
put_stress_set: str = "COMMON_SETTINGS:"
# После NL_STATIC_PARAMS: вставится set_solid
put_set_solid: str = "NL_STATIC_PARAMS:"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))