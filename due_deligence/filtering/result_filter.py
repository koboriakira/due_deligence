from abc import ABCMeta, abstractmethod
from typing import Dict


class ResultFilter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, results: Dict) -> Dict:
        raise NotImplementedError
