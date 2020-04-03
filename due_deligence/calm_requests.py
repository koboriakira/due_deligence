import requests
import time

session = requests.Session()


def get(url: str) -> requests.Response:
    """
    必ず1秒待つことでサーバ負荷を抑える
    """
    time.sleep(1)
    return session.get(url, stream=True)
