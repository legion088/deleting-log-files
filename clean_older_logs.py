import os
from datetime import datetime
from os.path import getsize, getmtime
import zipfile as zip
import json


def write_logs(info: dict):
    info = json.dumps(info, indent=4)
    with open('logs.json', 'w') as f_logs:
        f_logs.write(info)


def clean_older_files(files: list) -> dict:
    for cnt, file in enumerate(files, start=1):
        try:
            os.remove(file)
        except PermissionError as p_err:
            raise PermissionError('No permissions to delete file!')
    return {
        'clean': cnt
    }


def backup_older_files(files: list):
    filename_compress = f'zip_files_{datetime.now().date()}.zip'
    with zip.ZipFile(filename_compress, 'w') as file_zip:
        for item in files:
            file_zip.write(item)


def get_info_files(files: list) -> dict:
    return {
        'number of old files': len(files),
        'size': round(sum(getsize(file) for file in files) / 1024 / 1024, 2)
    }


def get_txt_logs_older_files(files: list) -> list:
    new_list_files = list()
    for file in files:
        if not file.endswith(('.txt', '.log')):
            continue

        last_modify = datetime.fromtimestamp(getmtime(file))
        if not (datetime.now() - last_modify).days > 7:
            continue
        new_list_files.append(file)
    return new_list_files


def get_files(abspath: str) -> list:
    if not os.path.join(abspath):
        raise FileNotFoundError('path not found!')

    older_files = list()
    for root, folders, files in os.walk(abspath):
        files = [os.path.join(root, file) for file in files]
        older_files.extend(get_txt_logs_older_files(files))
    return older_files


def main():
    logs = dict()
    abspath = r'C:\Users\petrov_pp\Desktop\files'
    files = get_files(abspath)

    if not files:
        raise ValueError('No files!')

    logs.update(get_info_files(files))
    backup_older_files(files)
    logs.update(clean_older_files(files))
    write_logs(logs)


if __name__ == '__main__':
    main()
