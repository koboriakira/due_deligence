from typing import Dict, List


class ResultStockPriceFilter(object):
    def __init__(self, stock_price: int):
        self._cond = stock_price

    def filter(self, results: Dict) -> Dict:
        result_dict = {}
        for sec_code, result in results.items():
            stock_price = result['stockPrice']
            if stock_price <= self._cond:
                result_dict[sec_code] = result
        return result_dict
