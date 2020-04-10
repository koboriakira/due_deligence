from due_deligence.domain_model.deligence import Deligence, DeligenceService
from due_deligence.domain_model.document import Document, DocumentService
from due_deligence.domain_model.stock import StockService
import sys
from logging import getLogger
from datetime import date
from copy import copy
import inject
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional
from tqdm import tqdm

logger = getLogger(__name__)


class DDController:
    def __init__(self, from_date: date, end_date: Optional[date] = None, sec_code_list: List[str] = []):
        self._from_date = from_date
        if end_date is None:
            self._end_date = copy(from_date)
        else:
            self._end_date = end_date
        self._sec_code_list = sec_code_list

        self._document_service = inject.instance(DocumentService)
        self._deligence_service = inject.instance(DeligenceService)
        self._stock_service = inject.instance(StockService)

    def execute(self) -> Dict:
        # if len(self._sec_code_list) > 0:
        #     self._pattern2(self._sec_code_list)
        #     return

        document_list = self._document_service.search(
            self._from_date, self._end_date)
        documents_as_sec_code = as_sec_code(document_list)
        logger.debug(documents_as_sec_code)

        doc_id_list = get_doc_id_list(document_list)
        report_map = self._deligence_service.search(doc_id_list)
        logger.debug(report_map)

        # todo: service化する？
        stock_map = self._stock_service.search(
            list(documents_as_sec_code.keys()))

        return create_due_deligence_dict(
            documents_as_sec_code, report_map, stock_map)

    # def _pattern2(self, sec_code_list: List[str]):
    #     document_list = self._document_service.search_by_sec_code(
    #         sec_code_list)
    #     documents_as_sec_code = as_sec_code(document_list)
    #     logger.info(documents_as_sec_code)

    #     doc_id_list = get_doc_id_list(document_list)
    #     report_map = self._deligence_service.search(doc_id_list)
    #     logger.info(report_map)

    #     print('- 現在の株価を取得していきます。%s秒かかる想定です。' %
    #           str(len(documents_as_sec_code.keys())))
    #     share_price_map = share_price_search(
    #         list(documents_as_sec_code.keys()))

    #     result_json = create_due_deligence_json(
    #         documents_as_sec_code, report_map, share_price_map)
    #     presenter = inject.instance(ResultPresenter)
    #     presenter.print(result_json)


def as_sec_code(document_list: List[Document]):
    result_map = {}
    for document in document_list:
        if document.sec_code() is None:
            continue

        document_list = get_document_list(result_map, document.sec_code())
        document_list.append(document)
        result_map[document.sec_code()] = document_list
    return result_map


def get_document_list(result_map, sec_code):
    if sec_code in result_map:
        return result_map[sec_code]
    return []


def get_doc_id_list(document_list: List[Document]):
    doc_id_list = []
    for document in document_list:
        doc_id_list.append(document.doc_id())
    return doc_id_list


def create_due_deligence_dict(documents_as_sec_code: Dict, report_map: Dict, stock_map: Dict) -> Dict:
    """
    株価の取得できた企業についてレポート結果をjson形式で返却
    """
    result_json = {}
    for sec_code in stock_map:
        filer_name = documents_as_sec_code[sec_code][0].filer_name()
        stock = stock_map[sec_code]
        due_deligences = []
        for document in documents_as_sec_code[sec_code]:
            if document.doc_id() not in report_map:
                due_deligence = {
                    'isError': True
                }
                due_deligences.append(due_deligence)
                continue
            report = report_map[document.doc_id()]
            underpriced = _underpriced(
                stock.share_price(), report.value_per_share())
            due_deligence = {
                'isError': False,
                'date': str(document.date()),
                'valueParShare': report.value_per_share(),
                'capitalRatio': report.capital_ratio(),
                'underpriced': underpriced
            }
            due_deligences.append(due_deligence)
        result_json[sec_code] = {
            'filerName': documents_as_sec_code[sec_code][0].filer_name(),
            'stockPrice': stock.share_price(),
            'due_deligences': due_deligences
        }
    return result_json


class ResultPresenter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def print(self, result: Dict) -> None:
        """
        分析結果を出力する
        """
        raise NotImplementedError

# 以下はリファクタして消す予定。


def _underpriced(stock_price, value_per_share):
    """
    安全圏、割安度を確認
    """
    return round(100 * stock_price / value_per_share, 0)


def share_price_search(sec_code_list: List[str]):
    share_price_map = {}
    for i in tqdm(range(len(sec_code_list))):
        sec_code = sec_code_list[i]
        share_price = scrape_stock_price(sec_code)
        if share_price is not None:
            share_price_map[sec_code] = share_price
    return share_price_map


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
    from due_deligence.util import calm_requests
    from bs4 import BeautifulSoup
    yahoo_stock_url = get_yahoo_stock_url(sec_code)
    response = calm_requests.get(yahoo_stock_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select('.m-stockPriceElm dl .now')[0].text.strip()


def get_yahoo_stock_url(sec_code: str):
    return 'https://www.nikkei.com/nkd/company/?scode=' + sec_code


def to_int(value: str):
    return int(float(value.replace(',', '').replace('円', '').strip()))
