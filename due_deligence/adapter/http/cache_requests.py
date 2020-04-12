from abc import ABCMeta, abstractmethod
import requests
import time
import percache

from .requests import Requests

cache = percache.Cache('.duedeligence_request_cache')


class CacheRequests(Requests):
    __metaclass__ = ABCMeta

    def __init__(self, wait_time=1):
        self._wait_time = wait_time

    @abstractmethod
    def get(self, url: str, stream=False):
        return _cache_get(url, stream, self._wait_time)


@cache
def _cache_get(url, stream, wait_time):
    print('cache')
    time.sleep(wait_time)
    return requests.get(url, stream=stream)
