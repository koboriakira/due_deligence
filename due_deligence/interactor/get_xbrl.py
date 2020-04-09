import os
import zipfile

from typing import List


def get_xbrl(path: List[str]) -> str:
    zip_extract(path)
    extracted_dir = '/tmp/' + path[1] + '/XBRL/PublicDoc'
    for file in os.listdir(extracted_dir):
        base, ext = os.path.splitext(file)
        if ext == '.xbrl':
            return extracted_dir + '/' + base + ext


def zip_extract(path: List[str]):
    zfile = zipfile.ZipFile('/' + path[0] + '/' + path[1] + '.zip')
    target_directory = '/' + path[0] + '/' + path[1]
    zfile.extractall(target_directory)
