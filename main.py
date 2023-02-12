from datetime import datetime
import os
from os.path import getmtime, join


def older_files(files: list, over_days=7) -> list:
    new_list_files = list()
    for file in files:
        last_modify = datetime.fromtimestamp(getmtime(file))
        if (datetime.now() - last_modify).days > over_days:
            new_list_files.append(file)
    return new_list_files


def get_files(path: str, extensions=('.tmp',)) -> list:
    if not os.path.exists(path):
        raise FileNotFoundError('Path not found!')
    new_list_files = list()
    for root, folder, files in os.walk(path):
        new_list_files.extend(join(root, file) for file in files if file.endswith(extensions))
    return new_list_files


if __name__ == '__main__':
    f = get_files('../files')
    older_files(f)
