from due_deligence.controller.dd_controller import ResultPresenter
from typing import Dict

UNDERPRICED_CONDITION = 50


class ResultTodayRecommendPresenter(object):
    def print(self, result: Dict, file_name='output'):
        print('安全圏50%以下の企業を一覧します')
        for sec_code in result:
            for due_deligence in result[sec_code]['due_deligences']:
                if 'underpriced' in due_deligence and due_deligence['underpriced'] > 0 and due_deligence['underpriced'] < 50:
                    print(sec_code, result[sec_code]['filerName'])
                    print('株価', result[sec_code]['stockPrice'], '円')
                    print('一株あたりの価値', due_deligence['valueParShare'], '円')
                    print('自己資本比率', due_deligence['capitalRatio'], '%')
                    print('安全圏', due_deligence['underpriced'], '%')
