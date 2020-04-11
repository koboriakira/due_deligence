from typing import Dict, List


class ResultUnderpricedFilter(object):
    def __init__(self, underpriced: int):
        self._underpriced_cond = underpriced

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
            underpriced = due_deligence['underpriced']
            if underpriced > 0 and underpriced <= self._underpriced_cond:
                result_list.append(due_deligence)
        return result_list
