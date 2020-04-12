from typing import Dict, List


class ResultCapitalRatioFilter(object):
    def __init__(self, capital_ratio: int):
        self._cond = capital_ratio

    def filter(self, results: Dict) -> Dict:
        result_dict = {}
        for sec_code, result in results.items():
            result['due_deligences'] = self._filter_due_deligences(
                result['due_deligences'])
            if len(result['due_deligences']) > 0:
                result_dict[sec_code] = result
        return result_dict

    def _filter_due_deligences(self, due_deligences: List) -> List:
        result_list = []
        for due_deligence in due_deligences:
            if due_deligence['isError']:
                continue
            capital_ratio = due_deligence['capitalRatio']
            if capital_ratio >= self._cond:
                result_list.append(due_deligence)
        return result_list
