#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, zipfile, urllib, datetime, shutil
from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection
from time import sleep


USERNAME='user'
PASSWORD='123456'
SERVER='192.168.60.187'
SHARE='public'


tmp_year = 2024
tmp_month = 1
tmp_day = 0


def upload_file(filename):
    folder_path = r'\\192.168.60.186\plm-bps'

    # создаём временный файл
    with open(f'backups\{filename}', 'w') as file:
        file.write('test')

    # копируем файл на сервер
    shutil.copy(f'backups\{filename}', folder_path)

    # удаляем временный файл
    os.remove(f'backups\{filename}')
    os.system(f'python main.py')

    
    


for i in range(0, 3600):
    if tmp_day < 28:
        tmp_day += 1
    else:
        tmp_day = 1
        tmp_month += 1

    if tmp_month == 13:
        tmp_year += 1
        tmp_month = 1


    day = str(tmp_day) if tmp_day > 9 else f'0{ tmp_day }'
    month = str(tmp_month) if tmp_month > 9 else f'0{ tmp_month }'
    year = str(tmp_year)

    filename = f'{ day }-{ month }-{ year }.zip'

    os.system(f'cls')

    print(f'\nCREATE: {filename}\n')
    # upload_file(USERNAME, PASSWORD, SERVER, SHARE, filename)
    upload_file(filename)
    sleep(0.3)



