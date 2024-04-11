#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os, psutil, subprocess
from pathlib import Path
from time import sleep


# Открываем диск Z
folder_path = r'\\test-bserv\plm-bps'


# if os.path.exists(folder_path) and os.path.isdir(folder_path):
#     # Получаем список файлов в папке
#     files = os.listdir(folder_path)
    
#     # Выводим содержимое папки
#     print(f"Содержимое папки: { files }")
#     for file in files:
#         print(file)
# else:
#     print("Указанный путь не существует или не является папкой.")

splm_serv = Path('C:/Program Files (x86)/Програмсоюз/BIS v3/Server')
file_proc = 'PLMFileServer.exe'
main_proc = 'PLMMainServer.exe'


def stop_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            print(f"Stopping process {process_name} (PID: {proc.info['pid']})")
            proc.kill()
            print(f"Process {process_name} stopped.")
            return
    print(f"Process {process_name} not found.")


stop_process(main_proc)
stop_process(file_proc)



sleep(5)


def start_process(process_name):
    # Пример команды для запуска процесса, замените на свою
    command = f"start {process_name}.exe"
    subprocess.Popen(command, shell=True)


start_process(f'{splm_serv}/{main_proc}')
start_process(f'{splm_serv}/{file_proc}')


