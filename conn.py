#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os, subprocess
from pathlib import Path


def backup_database(server, database, backup_path):
    # Строка подключения к базе данных
    conn_str = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;'
    
    
    # Команда для создания резервной копии
    backup_cmd = f'sqlcmd -S {server} -d {database} -E -Q "BACKUP DATABASE [{database}] TO DISK=\'{backup_path}\'"'
    
    print('CMD: ', backup_cmd)

    # Выполнение команды
    os.system(f"echo > { Path('C:/PLM-DATA.bak' )}")
    subprocess.run(backup_cmd, shell=True)
    



# backup_path=Path('C:/Users/anon/dev/backup-app/tmp/PLM-DATA.bak')
backup_database(server='localhost', database='PLM-DATA', backup_path=Path('C:/PLM-DATA.bak'))
