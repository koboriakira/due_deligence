from abc import ABCMeta, abstractmethod
from typing import List, Dict


class Stock:
    def __init__(self, share_price):
        self._share_price = share_price

    def share_price(self):
        return self._share_price


class StockService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, sec_code_list: List[str]) -> Dict:
        """
        企業コード別の株式情報を取得します
        """
        raise NotImplementedError
