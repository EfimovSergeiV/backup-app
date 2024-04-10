#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Порядок выполнения резервного копирования:

    1. Останавливаем процессы 
    2. Создаём дамп базы данных
    3. Архивируем файлы + дамп базы данных
    4. Загружаем архив на smb сервер
    5. Удаляем старые архивы
    6. Запускаем процессы

"""

from pathlib import Path
import sys, os, zipfile, datetime
from methods import (
    get_list_files, 
    remove_files,
    create_zip,
    backup_database
)


BASE_DIR = Path(__file__).resolve().parent.parent


# Количество файлов, которые должны оставаться на сервере 20
AMOUNT_FILES_DAY = 5
AMOUNT_FILES_MONTH = 12
AMOUNT_FILES_YEAR = 3

MONTH_BACKUP_DATE = '15'
YEAR_BACKUP_DATE = '10-09'

SERVER = r'\\192.168.60.186\plm-bps'


PLMClientConfig = Path('C:/Program Files (x86)/Програмсоюз/BIS v3/PLMClient.exe.config')
    

backups = {}
remove_list = []



# Раскладываем файлы по годам
# for file in  get_list_files(SERVER):
#     if file.split('.')[0].split('-')[2] in backups:
#         backups[file.split('.')[0].split('-')[2]].append(file)
#     else:
#         backups[file.split('.')[0].split('-')[2]] = [file]

# # Сортируем файлы по дате
# for key, value in backups.items():
#     value.sort(key=lambda x: datetime.datetime.strptime(x.split('.')[0], '%d-%m-%Y'), reverse=True)


# # Сортируем года по убыванию для спокойствия
# order_years = [ int(year) for year in backups.keys() ]
# order_years.sort(reverse=True)


# # Создаём список файлов на удаление
# for key, items in backups.items():
#     tmp_list = []

#     if int(key) == order_years[0]: # Проверка на последний год в архивах
#         for file in items:
#             if file.split('.')[0].split('-')[0] != MONTH_BACKUP_DATE:
#                 tmp_list.append(file)

#         remove_list += tmp_list[AMOUNT_FILES_DAY:]

#     elif len(order_years) > 1 and int(key) == order_years[1]:
#         for file in items:
#             if file.split('.')[0].split('-')[0] != MONTH_BACKUP_DATE:
#                 tmp_list.append(file)

#         remove_list += tmp_list

#     elif len(order_years) > 2 and int(key) == order_years[2]:
#         for file in items:
#             if file.split('.')[0].split('-')[0] != MONTH_BACKUP_DATE:
#                 tmp_list.append(file)

#         remove_list += tmp_list    

#     else:
#         for file in items:
#             tmp_list.append(file)
        
#         remove_list += tmp_list



# for key, items in backups.items():
#     print(key, items)
# """
# CREATE: 16-09-2033.zip

# 2033 ['16-09-2033.zip', '15-09-2033.zip', '14-09-2033.zip', '13-09-2033.zip', '12-09-2033.zip', '11-09-2033.zip', '10-09-2033.zip', '15-08-2033.zip', '15-07-2033.zip', '15-06-2033.zip', '15-05-2033.zip', '15-04-2033.zip', '15-03-2033.zip', '15-02-2033.zip', '15-01-2033.zip']
# 2032 ['15-12-2032.zip', '15-11-2032.zip', '15-10-2032.zip', '15-09-2032.zip', '15-08-2032.zip', '15-07-2032.zip', '15-06-2032.zip', '15-05-2032.zip', '15-04-2032.zip', '15-03-2032.zip', '15-02-2032.zip', '15-01-2032.zip']
# 2031 ['15-12-2031.zip', '15-11-2031.zip', '15-10-2031.zip', '15-09-2031.zip', '15-08-2031.zip', '15-07-2031.zip', '15-06-2031.zip', '15-05-2031.zip', '15-04-2031.zip', '15-03-2031.zip', '15-02-2031.zip', '15-01-2031.zip']
# """

# #remove_status = remove_files(SERVER, remove_list)




backup_database(server='localhost', database='PLM-DATA', backup_path=Path('C:/PLM-DATA.bak'))
create_zip(source_dir= Path('C:\PLMFILES'), output_file= Path('C:/PLM-BACKUP.zip'))
