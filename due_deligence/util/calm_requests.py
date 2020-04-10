import requests
import time


def get(url: str):
    """
    必ず1秒待つことでサーバ負荷を抑える
    """
    time.sleep(1)
    return requests.get(url, stream=True)
