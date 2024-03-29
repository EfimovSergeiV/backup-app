#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, zipfile, urllib, datetime
from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Количество файлов, которые должны оставаться на сервере 20
AMOUNT_FIES_DAY = 5
AMOUNT_FIES_MONTH = 12
AMOUNT_FIES_YEAR = 3


now = datetime.datetime.now().strftime('%d-%m-%Y-')
source_dir = os.path.join(BASE_DIR, 'source')
output_filename = os.path.join(BASE_DIR, 'backups', f'{ now }.zip')


# Создаём новый архив
def create_zip(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_dir))


# Выгрузка нового архива на smb сервер
def upload_file(username, password, server, share, filename):
    file_fh = open(output_filename, 'rb')
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(f'smb://{ username }:{ password }@{ server }/{ share }/backups/{ filename }', data = file_fh)
    fh.close()


# Получаем список архивов на smb сервере
def get_list_files(username, password, server, share):
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



# create_zip(source_dir, output_filename)
# upload_file(username='user', password='123456', server='192.168.60.187', share='public', filename=f'{ now }.zip')
# get_list_files(username='user', password='123456', server='192.168.60.187', share='public')
    

