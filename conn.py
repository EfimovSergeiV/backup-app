#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from pathlib import Path


folder_path = r'\\192.168.60.186\plm-bps'


if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Получаем список файлов в папке
    files = os.listdir(folder_path)
    
    # Выводим содержимое папки
    print(f"Содержимое папки: { files }")
    for file in files:
        print(file)
else:
    print("Указанный путь не существует или не является папкой.")





