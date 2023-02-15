from datetime import datetime
import os
from os.path import getmtime, join, getsize
import zipfile as zip


def clean_files(files: list) -> dict:
    for cnt, file in enumerate(files, start=1):
        try:
            os.remove(file)
        except PermissionError:
            raise PermissionError('No permissions to delete file!')
    return {
        'clean': cnt
    }


def backup_files(files: list) -> None:
    filename_compress = f'zip_files_{datetime.now().date()}.7z'
    with zip.ZipFile(filename_compress, 'w') as file_zip:
        for item in files:
            file_zip.write(item)


def get_info_files(files: list) -> dict:
    return {
        'number of old files': len(files),
        'size': round(sum(getsize(file) for file in files) / 1024 / 1024, 2)
    }


def get_files_over_days(files: list, over_days=7) -> list:
    new_list_files = list()
    for file in files:
        last_modify = datetime.fromtimestamp(getmtime(file))
        if (datetime.now() - last_modify).days > over_days:
            new_list_files.append(file)
    return new_list_files


def get_files(path: str, extensions=('.txt', '.log')) -> list:
    try:
        new_list_files = list()
        for root, folder, files in os.walk(path):
            new_list_files.extend(join(root, file) for file in files if file.endswith(extensions))
    except FileNotFoundError:
        raise FileNotFoundError('Path not found!')
    return new_list_files


if __name__ == '__main__':
    files = get_files('../filles')
    files = get_files_over_days(files)
    get_info_files(files)
    backup_files(files)
    clean_files(files)	