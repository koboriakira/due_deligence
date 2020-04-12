from abc import ABCMeta, abstractmethod
import requests
import time


class Requests(object):
    __metaclass__ = ABCMeta

    def __init__(self, wait_time=1):
        self._wait_time = wait_time

    @abstractmethod
    def get(self, url: str, stream=False):
        time.sleep(self._wait_time)
        return requests.get(url, stream=stream)
