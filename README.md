# Удаление лог файлов
1. Выполняем поиск файлов расширениями в аргументе `extensions=('.txt', '.log')`, и старше N дней в аргументе `over_days=7`.
2. Делаем резервную копию удаляемых файлов, и сжимаем их с помощью zipfile.
3. Удаляем файлы 

# Deleting log files
1. Search for files with extensions in the extensions=('.txt', '.log') argument, and older than N days in the over_days=7 argument..
2. Make a backup copy of the deleted files, and compress them using zipfile.
3. Delete files
