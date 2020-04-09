import logging
import random
import string
import zipfile
import os
from typing import List
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser

from due_deligence.util import calm_requests as requests
from due_deligence.adapter.deligence import XbrlDownloader

DIR = 'tmp'

class XbrlObjDownloader(object):
  def get(self, doc_id: str):
    detail_url = self._generate_doc_url(doc_id)

    # XBRLの取得
    path = self._download_file(detail_url)
    print(path)
    if not path:
        logging.error('エラー！ ファイルが取得または開くことができませんでした')
        return None

    xbrl_path = get_xbrl(path)
    parser = EdinetXbrlParser()
    return parser.parse_file(xbrl_path)

  def _generate_doc_url(self, doc_id:str):
    # ex.) https://disclosure.edinet-fsa.go.jp/api/v1/documents/S100IA9D?type=1
    return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/' + doc_id + '?type=1'

  def _download_file(self, url: str) -> List[str]:
      """
      URL を指定してカレントディレクトリにファイルをダウンロードする
      """

      filename = randomname(10)
      filepath = '/' + DIR + '/' + filename + '.zip'
      r = requests.get(url)
      with open(filepath, 'wb') as f:
          for chunk in r.iter_content(chunk_size=1024):
              if chunk:
                  f.write(chunk)
                  f.flush()
          return [DIR, filename]

      # ファイルが開けなかった場合は False を返す
      return False

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


def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits)
            for i in range(n)]
    return ''.join(randlst)
