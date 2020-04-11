from due_deligence.domain_model.stock import StockService
from due_deligence.util.progress_presenter import ProgressPresenter
import inject
from logging import getLogger
from due_deligence.util import calm_requests
from bs4 import BeautifulSoup
from due_deligence.domain_model.stock import Stock
from typing import List, Dict

logger = getLogger(__name__)


class SimpleStockService(StockService):
    def __init__(self):
        self._progress_presenter = inject.instance(ProgressPresenter)

    def search(self, sec_code_list: List[str]) -> Dict:
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
            soup = get_soup(sec_code)
            share_price = get_share_price(soup)
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


def get_soup(sec_code: str):
    url = get_url(sec_code)
    response = get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_share_price(soup: BeautifulSoup) -> int:
    value = soup.select('.m-stockPriceElm dl .now')[0].text.strip()
    return to_int(value)


def get(url: str):
    return calm_requests.get(url)


def get_url(sec_code: str):
    return 'https://www.nikkei.com/nkd/company/?scode=' + sec_code


def to_int(value: str):
    return int(float(value.replace(',', '').replace('円', '').strip()))
