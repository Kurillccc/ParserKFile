import click
import os
from app.parser import parse_k_file, parse_cd_file
from app.processor import group_elements_by_layer

@click.command()
@click.option("--input", default="data/input", help="Папка с исходными файлами")
@click.option("--output", default="data/output", help="Папка для сохранения")
def run(input, output):
    k_file = os.path.join(input, "test0.k")
    cd_file = os.path.join(input, "test0.cd")

    print("Чтение файлов...")
    parse_k_file(k_file)
    parse_cd_file(cd_file)



    print("Выполнено")

if __name__ == "__main__":
    run()
