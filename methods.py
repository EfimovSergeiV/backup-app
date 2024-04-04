#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, zipfile, urllib, datetime
from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection


def get_list_files(username, password, server, share):
    """
    Возвращает список файлов на сервере
    """
    list_files = []
    conn = SMBConnection(username, password, "pysmb", server, use_ntlm_v2=True)
    conn.connect(server, 445)
    try:
        file_list = conn.listPath(share, "backups")
        for item in file_list:
            if not item.isDirectory and item.filename.endswith('.zip'):
                list_files.append(item.filename)
    except Exception as e:
        print("Ошибка при получении списка файлов:", e)

    list_files.sort(key=lambda x: datetime.datetime.strptime(x.split('.')[0], '%d-%m-%Y'), reverse=True)
    conn.close()

    return list_files


def remove_files(username, password, server, share, list_files):
    """
    Удаляет файлы с сервера
    """
    conn = SMBConnection(username, password, "pysmb", server, use_ntlm_v2=True)
    conn.connect(server, 445)
    try:
        for file in list_files:
            conn.deleteFiles(share, f'backups/{ file }')
    except Exception as e:
        print(f'Ошибка при удалении файла { file }: { e }')

    conn.close()
    return True









# Создаём новый архив
def create_zip(source_dir, OUTPUT_FILE):
    with zipfile.ZipFile(OUTPUT_FILE, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_dir))


# Выгрузка нового архива на smb сервер
def upload_file( username, password, server, share, filename, OUTPUT_FILE=None):
    file_fh = open(OUTPUT_FILE, 'rb')
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(f'smb://{ username }:{ password }@{ server }/{ share }/backups/{ filename }', data = file_fh)
    fh.close()




# Удаление лишних файлов
def del_files(list_files, conn, share):
    
    for file in list_files:
        try:
            # Удаление файла, если он не сделан первого числа месяца
            if file.split('.')[0].startswith('01'):
                continue
            conn.deleteFiles(share, f'backups/{ file }')
            print(f'Файл { file } удален')

        except Exception as e:
            print(f'Ошибка при удалении файла { file }: { e }')