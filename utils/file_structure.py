import os
import json
from typing import List

from references.paths import get_main_folder_path


def get_forbidden_folders() -> List[str]:
    return ["venv"]


def get_file_structure(folder_path):
    forbidden_folders = get_forbidden_folders()
    folder_name = os.path.basename(folder_path)
    dir_structure = {}
    file_structure = {}

    for item in sorted(os.listdir(folder_path)):
        if item in forbidden_folders:
            continue
        if item.startswith('.') or item.startswith('__'):
            continue
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_structure[item] = 'file'
        elif os.path.isdir(item_path):
            nested_structure = get_file_structure(item_path)
            if nested_structure:
                dir_structure[item] = nested_structure

    return {**dir_structure, **file_structure}


def __main():
    root_folder = get_main_folder_path()
    file_structure = get_file_structure(root_folder)

    output_json = json.dumps(file_structure, indent=4)
    print(output_json)


if __name__ == "__main__":
    __main()
