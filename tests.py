#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, zipfile, urllib, datetime
from smb.SMBHandler import SMBHandler
from smb.SMBConnection import SMBConnection
from time import sleep


USERNAME='user'
PASSWORD='123456'
SERVER='192.168.60.187'
SHARE='public'


tmp_year = 2023
tmp_month = 1
tmp_day = 0


def upload_file(username, password, server, share, filename):

    # создаём файл
    with open(f'backups/{filename}', 'w') as file:
        file.write('test')

    file_fh = open(f'backups/{filename}', 'rb')
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(f'smb://{ username }:{ password }@{ server }/{ share }/backups/{ filename }', data = file_fh)
    fh.close()

    os.remove(f'backups/{filename}')
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

    os.system(f'clear')

    print(f'\nCREATE: {filename}\n')
    upload_file(USERNAME, PASSWORD, SERVER, SHARE, filename)
    sleep(0.5)



