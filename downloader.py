#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from cStringIO import StringIO
from baidupcsapi import PCS
import wget
import os
import hashlib
import getpass
import platform

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


def md5sum(file_name):
    return hashfile(open(file_name, 'rb'), hashlib.md5())


server_dir = '/'
out_dir = './Output/'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

id_str = raw_input('id > ')
pw_str = getpass.getpass('password > ')

if platform.system() == 'Windows':
    try:
        from PIL import Image
    except:
        import Image
    from img2txt import img2txt

    def captcha(img):
        jpeg_data = StringIO(img)
        print img2txt(jpeg_data)
        # im = Image.open(jpeg_data)
        # im.show()
        return raw_input('capcha > ')

    pcs = PCS(id_str, pw_str, captcha)
else:
    pcs = PCS(id_str, pw_str)

response = pcs.list_files(server_dir)
json_response = response.json()
file_list = json_response['list']

for file_meta in file_list:
    full_path = file_meta['path']
    file_name = file_meta['server_filename']
    md5 = file_meta['md5']

    print 'File:', full_path

    if os.path.exists(out_dir + file_name):
        local_md5 = md5sum(out_dir + file_name)
        print 'file exists'
        print 'server md5:', md5
        print ' local md5:', local_md5

        if md5 == local_md5:
            print 'skip file'
            continue

    download_url = pcs.download_url(full_path)[0]
    wget.download(download_url, out=out_dir)
    print ' '
