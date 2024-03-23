#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, zipfile, urllib, datetime
from smb.SMBHandler import SMBHandler


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
source_dir = os.path.join(BASE_DIR, 'source')
output_filename = os.path.join(BASE_DIR, 'backups', f'{now}.zip')


# Create a zip file from a directory
def create_zip(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_dir))


# Upload a file to a remote server
def upload_file(username, password, server, share, filename):
    file_fh = open(output_filename, 'rb')
    director = urllib.request.build_opener(SMBHandler)
    fh = director.open(f'smb://{username}:{password}@{server}/{share}/backups/{filename}', data = file_fh)
    fh.close()


create_zip(source_dir, output_filename)
upload_file(username='user', password='123456', server='192.168.60.187', share='public', filename=f'{now}.zip')