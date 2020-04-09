from due_deligence.controller.dd_controller import ResultPresenter
from typing import Dict
import json


class ResultScreenPresenter(object):
    def print(self, result: Dict, file_name='output'):
        print(result)
        f = open(file_name + '.json', "w")
        json.dump(result, f, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
