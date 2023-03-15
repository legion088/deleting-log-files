from datetime import datetime
from typing import Union
from os.path import join, getsize, getmtime
import os
import zipfile as zip

"""
Условие: .days > over_days
Пример: 16(сколько дней файлу) > 14(аргумент over_days) -> файл попадет 
"""


class FileObject:
    def __init__(self, path: str, extension: Union[str, tuple]):
        self.path = path
        self.extension = extension

    def get_files(self) -> list:
        ls_files = []
        try:
            for root, folder, files in os.walk(self.path):
                ls_files.extend(join(root, file)
                                for file in files if file.endswith(self.extension))
        except FileNotFoundError:
            raise FileNotFoundError('Path not found!')
        return ls_files

    def get_older_files(self, over_days=30) -> list:
        ls_files = [file for file in self.get_files()
                    if (datetime.now() - datetime.fromtimestamp(getmtime(file))).days > over_days]
        return ls_files

    @staticmethod
    def backup_files(files: list) -> None:
        filename_compress = f'zip_files_{datetime.now().date()}.7z'
        with zip.ZipFile(filename_compress, 'w') as file_zip:
            for item in files:
                file_zip.write(item)

    @staticmethod
    def clean_files(files: list) -> dict:
        for cnt, file in enumerate(files, start=1):
            try:
                os.remove(file)
            except PermissionError:
                raise PermissionError('No permissions to delete file!')
        return {
            'clean': cnt
        }

    @staticmethod
    def output_info_files(files: list) -> dict:
        return {
            'number files': len(files),
            'size': round(sum(getsize(file) for file in files) / 1024 / 1024, 2)
        }


if __name__ == 'main':
   example_host = FileObject(r'../files', ('.txt', '.log'))
   older_files = example_host.get_older_files()
   print(example_host.output_info_files(older_files))

