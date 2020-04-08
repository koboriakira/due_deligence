import random
import string
from typing import List
from due_deligence import calm_requests

# @see http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py

DIR = 'tmp'


def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return ''.join(randlst)


def download_file(url: str) -> List[str]:
    """
    URL を指定してカレントディレクトリにファイルをダウンロードする
    """

    filename = randomname(10)
    filepath = '/' + DIR + '/' + filename + '.zip'
    r = calm_requests.get(url)
    with open(filepath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return [DIR, filename]

    # ファイルが開けなかった場合は False を返す
    return False
