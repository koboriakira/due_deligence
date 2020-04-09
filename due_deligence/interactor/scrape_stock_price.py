from bs4 import BeautifulSoup
import logging
from due_deligence.interactor.company import Company
from due_deligence import calm_requests


YAHOO_URL = 'https://stocks.finance.yahoo.co.jp/stocks/detail/?code=7751.T'


def scrape_stock_price(company: Company):
    if company.sec_code is None:
        logging.warning('企業コード不明のため、株価を取得できませんでした。')
        return None

    try:
        value = scrape_value(company.sec_code)
        return to_int(value)
    except IndexError:
        logging.warning('現在の株価が取得できませんでした')
        return None
    except ValueError:
        logging.warning('現在の株価が存在しませんでした')
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
