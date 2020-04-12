from due_deligence.domain_model.stock import StockService
from due_deligence.util.progress_presenter import ProgressPresenter
import inject
from logging import getLogger
from bs4 import BeautifulSoup
from due_deligence.domain_model.stock import Stock
from typing import List, Dict
from due_deligence.adapter.http.requests import Requests

logger = getLogger(__name__)


class SimpleStockService(StockService):
    def __init__(self):
        self._progress_presenter = inject.instance(ProgressPresenter)
        self._requests = inject.instance(Requests)

    def search(self, sec_code_list: List[str]) -> Dict:
        if len(sec_code_list) == 0:
            return {}
        self._progress_presenter.print('- 現在の株価を取得していきます')
        stock_map = {}
        for i in self._progress_presenter.wrap_tqdm(range(len(sec_code_list))):
            sec_code = sec_code_list[i]
            stock = self._get_stock(sec_code)
            if stock is not None:
                stock_map[sec_code] = stock
        return stock_map

    def _get_stock(self, sec_code: str) -> Stock:
        try:
            soup = self._get_soup(sec_code)
            share_price = self._get_share_price(soup)
            return Stock(share_price)
        except IndexError:
            logger.warning('現在の株価が取得できませんでした')
            return None
        except ValueError:
            logger.warning('現在の株価が存在しませんでした')
            return None
        except:
            logger.error('その他エラー')
            return None

    def _get_soup(self, sec_code: str):
        url = get_url(sec_code)
        response = self._get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def get(self, url: str):
        return self._requests.get(url)

    def _get_share_price(self, soup: BeautifulSoup) -> int:
        value = soup.select('.m-stockPriceElm dl .now')[0].text.strip()
        return to_int(value)


def get_url(sec_code: str):
    return 'https://www.nikkei.com/nkd/company/?scode=' + sec_code


def to_int(value: str):
    return int(float(value.replace(',', '').replace('円', '').strip()))
