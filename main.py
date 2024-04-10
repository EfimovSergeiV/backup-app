#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import os, datetime, shutil
from methods import ( get_list_files, remove_files, create_zip, backup_database)


BASE_DIR = Path(__file__).resolve().parent.parent


# Количество файлов, которые должны оставаться на сервере 20
AMOUNT_FILES_DAY = 5
AMOUNT_FILES_MONTH = 12
AMOUNT_FILES_YEAR = 3

MONTH_BACKUP_DATE = '15'
YEAR_BACKUP_DATE = '10-09'

SERVER = r'\\192.168.60.186\plm-bps'

    

backups = {}
remove_list = []

# Поиск и удаление неактуальных архивов
# Раскладываем файлы по годам
for file in get_list_files(SERVER):
    if file.split('.')[0].split('-')[2] in backups:
        backups[file.split('.')[0].split('-')[2]].append(file)
    else:
        backups[file.split('.')[0].split('-')[2]] = [file]

# Сортируем файлы по дате
for key, value in backups.items():
    value.sort(key=lambda x: datetime.datetime.strptime(x.split('.')[0], '%d-%m-%Y'), reverse=True)


# Сортируем года по убыванию для спокойствия
order_years = [ int(year) for year in backups.keys() ]
order_years.sort(reverse=True)


# Создаём список файлов на удаление
for key, items in backups.items():
    tmp_list = []

    if int(key) == order_years[0]: # Проверка на последний год в архивах
        for file in items:
            if file.split('.')[0].split('-')[0] != MONTH_BACKUP_DATE:
                tmp_list.append(file)

        remove_list += tmp_list[AMOUNT_FILES_DAY-1:]

    elif len(order_years) > 1 and int(key) == order_years[1]:
        for file in items:
            if file.split('.')[0].split('-')[0] != MONTH_BACKUP_DATE:
                tmp_list.append(file)

        remove_list += tmp_list

    elif len(order_years) > 2 and int(key) == order_years[2]:
        for file in items:
            if file.split('.')[0].split('-')[0] != MONTH_BACKUP_DATE:
                tmp_list.append(file)

        remove_list += tmp_list    

    else:
        for file in items:
            tmp_list.append(file)
        
        remove_list += tmp_list


remove_files(SERVER, remove_list)



now = '02-05-2024.zip'

# Создание свежей резервной копии
bkp_completed = backup_database(server='localhost', database='PLM-DATA', backup_path=Path('C:/PLM-DATA.bak'))

if bkp_completed:
    create_zip(output_file= Path(f'C:/{ now }'))


# Выгрузка архива на smb сервер
shutil.copy(Path(f'C:/{ now }'), SERVER)
os.system(f"del { Path(f'C:/{ now }') }")