from due_deligence.controller.dd_controller import ResultPresenter
from typing import Dict
import json


class ResultScreenPresenter(object):
    def print(self, result: Dict):
        for sec_code in result:
            filer_name = result[sec_code]['filerName']
            share_price = str(result[sec_code]['stockPrice'])
            print(
                f'*************** {sec_code} {filer_name} 株価: {share_price}円 ***************')
            for due_deligence in result[sec_code]['due_deligences']:
                date = due_deligence['date']
                value_per_share = due_deligence['valueParShare']
                capital_ratio = due_deligence['capitalRatio']
                underpriced = due_deligence['underpriced']
                print(f'- {date}提出')
                print(f'    - 一株あたりの価値: {value_per_share}円')
                print(f'    - 自己資本比率: {capital_ratio}%')
                print(f'    - 安全圏: {underpriced}%')
