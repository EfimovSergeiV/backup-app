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

splm_serv = 'C:/Program Files (x86)/Програмсоюз/BIS v3/Server'
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



sleep(15)


subprocess.Popen(r"C:\Program Files (x86)\Програмсоюз\BIS v3\Server\PLMMainServer.exe")
subprocess.Popen(r"C:\Program Files (x86)\Програмсоюз\BIS v3\Server\PLMFileServer.exe")