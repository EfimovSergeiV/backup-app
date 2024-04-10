#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, zipfile, subprocess, datetime
from pathlib import Path



def get_list_files(folder_path):
    """ Возвращает список .zip архивов на сервере """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        list_files = []
        for item in os.listdir(folder_path):
            if item.endswith('.zip'):
                list_files.append(item)
        return list_files


def remove_files(folder_path, list_files):
    """ Удаляет файлы с сервера """
    for file in list_files:
        try:
            os.remove(f'{ folder_path }/{ file }')
        except Exception as e:
            print(f'Ошибка при удалении файла { file }: { e }')
    return True


def backup_database(server, database, backup_path):
    """ Создаёт резервную копию базы данных """
    backup_cmd = f'sqlcmd -S {server} -d {database} -E -Q "BACKUP DATABASE [{database}] TO DISK=\'{backup_path}\'"'
    os.system(f"echo > { Path('C:/PLM-DATA.bak' )}")
    subprocess.run(backup_cmd, shell=True)
    return True


def create_zip(output_file):
    """ Создаёт архив из файлов """
    with zipfile.ZipFile(output_file, 'w') as zipf:
        for root, dirs, files in os.walk(Path('C:\PLMFILES')):
            for file in files:
                zipf.write(os.path.join(root, file), 'PLMFILES\\' + os.path.relpath(os.path.join(root, file), Path('C:\PLMFILES')))
        zipf.write(Path('C:/PLM-DATA.bak'))
        zipf.write(Path('C:/Program Files (x86)/Програмсоюз/BIS v3/PLMClient.exe.config'), 'PLMClient.exe.config')

    os.system(f"del { Path('C:/PLM-DATA.bak') }")

    return True
