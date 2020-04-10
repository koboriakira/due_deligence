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
            share_price = scrape_stock_price(sec_code)
            if share_price is not None:
                stock = Stock(share_price)
                stock_map[sec_code] = stock
        return stock_map


def scrape_stock_price(sec_code: str):
    try:
        value = scrape_value(sec_code)
        return to_int(value)
    except IndexError:
        logger.warning('現在の株価が取得できませんでした')
        return None
    except ValueError:
        logger.warning('現在の株価が存在しませんでした')
        return None
    except:
        logger.error('その他エラー')
        return None


def scrape_value(sec_code: str):
    yahoo_stock_url = get_yahoo_stock_url(sec_code)
    response = calm_requests.get(yahoo_stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select('.m-stockPriceElm dl .now')[0].text.strip()


def get_yahoo_stock_url(sec_code: str):
    return 'https://www.nikkei.com/nkd/company/?scode=' + sec_code


def to_int(value: str):
    return int(float(value.replace(',', '').replace('円', '').strip()))
