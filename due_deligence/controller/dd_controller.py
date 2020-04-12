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
from due_deligence.filtering.result_filter import ResultFilter

logger = getLogger(__name__)


class DDController:
    def __init__(self, from_date: date, end_date: Optional[date] = None, sec_code_list: List[str] = [], filters: List[ResultFilter] = []):
        self._from_date = from_date
        if end_date is None:
            self._end_date = copy(from_date)
        else:
            self._end_date = end_date
        self._sec_code_list = sec_code_list

        self._document_service = inject.instance(DocumentService)
        self._deligence_service = inject.instance(DeligenceService)
        self._stock_service = inject.instance(StockService)
        self._filters = filters

    def execute(self) -> Dict:
        document_list = self._document_service.search(
            self._from_date, self._end_date)
        documents_as_sec_code = as_sec_code(document_list)
        logger.debug(documents_as_sec_code)

        doc_id_list = get_doc_id_list(document_list)
        report_map = self._deligence_service.search(doc_id_list)
        logger.debug(report_map)

        stock_map = self._stock_service.search(
            list(documents_as_sec_code.keys()))

        results = create_due_deligence_dict(
            documents_as_sec_code, report_map, stock_map)
        for f in self._filters:
            results = f.filter(results)
        return results


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


def _underpriced(stock_price: int, value_per_share: int) -> int:
    """
    安全圏、割安度を確認
    """
    try:
        return round(100 * stock_price / value_per_share, 0)
    except ZeroDivisionError as e:
        logger.warning('ゼロ除算')
        return 0
