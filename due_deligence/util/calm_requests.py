import requests
import time
import percache

cache = percache.Cache('.duedeli_request_cache')


@cache
def get(url: str):
    """
    必ず1秒待つことでサーバ負荷を抑える
    また結果をキャッシュしておくことで同じURLのリクエストにはそのまま返す
    """
    time.sleep(1)
    return requests.get(url, stream=True)
