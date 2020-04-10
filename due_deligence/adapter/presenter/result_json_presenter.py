from due_deligence.controller.dd_controller import ResultPresenter
from typing import Dict
import json


class ResultJsonPresenter(object):
    def __init__(self, file_path):
        self._file_path = file_path

    def print(self, result: Dict):
        f = open(self._file_path, "w")
        json.dump(result, f, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
