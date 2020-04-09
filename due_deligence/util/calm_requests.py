import requests
import time

from due_deligence.config import WAIT_TIME

session = requests.Session()

def get(url: str):
    """
    必ず1秒待つことでサーバ負荷を抑える
    """
    time.sleep(WAIT_TIME)
    return session.get(url, stream=True)
