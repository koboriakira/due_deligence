from due_deligence.interactor.due_deligence_requester import DueDeligenceRequester
from due_deligence.domain_model.deligence import Deligence, DeligenceService
from due_deligence.domain_model.document import Document, DocumentService
import sys
import logging
from datetime import date
from copy import copy
import inject
from abc import ABCMeta, abstractmethod
from typing import Dict, List


def pattern1(target_date_str):
    target_date = date.fromisoformat(target_date_str)

    document_service = inject.instance(DocumentService)
    document_list = document_service.search(target_date, copy(target_date))
    documents_as_sec_code = as_sec_code(document_list)
    print(documents_as_sec_code)

    deligence_service = inject.instance(DeligenceService)
    print(len(document_list), '秒待つ')
    doc_id_list = get_doc_id_list(document_list)
    report_map = deligence_service.search(doc_id_list)
    print(report_map)

    # todo: service化する？
    print(len(documents_as_sec_code.keys()), '秒待つ')
    share_price_map = share_price_search(documents_as_sec_code.keys())
    print(share_price_map)

    result_json = create_due_deligence_json(
        documents_as_sec_code, report_map, share_price_map)
    presenter = inject.instance(ResultPresenter)
    presenter.print(result_json, file_name=target_date_str)


def pattern2(sec_code_list: List[str]):
    document_service = inject.instance(DocumentService)
    document_list = document_service.search_by_sec_code(sec_code_list)
    documents_as_sec_code = as_sec_code(document_list)
    print(documents_as_sec_code)

    deligence_service = inject.instance(DeligenceService)
    print(len(document_list), '秒待つ')
    doc_id_list = get_doc_id_list(document_list)
    report_map = deligence_service.search(doc_id_list)
    print(report_map)

    # todo: service化する？
    print(len(documents_as_sec_code.keys()), '秒待つ')
    share_price_map = share_price_search(documents_as_sec_code.keys())
    print(share_price_map)

    result_json = create_due_deligence_json(
        documents_as_sec_code, report_map, share_price_map)
    presenter = inject.instance(ResultPresenter)
    presenter.print(result_json, file_name='selected.csv')


def pattern3(from_date_str: str, end_date_str: str):
    from_date = date.fromisoformat(from_date_str)
    end_date = date.fromisoformat(end_date_str)

    print('- xbrlファイルの一覧を取得します。')
    document_service = inject.instance(DocumentService)
    document_list = document_service.search(from_date, copy(end_date))
    documents_as_sec_code = as_sec_code(document_list)
    logging.info(documents_as_sec_code)

    print('- ファイルの解析を行います。%s秒かかる想定です。' % str(len(document_list)))
    deligence_service = inject.instance(DeligenceService)
    doc_id_list = get_doc_id_list(document_list)
    report_map = deligence_service.search(doc_id_list)
    logging.info(report_map)

    # No presentation
    print('- 完了しました!')


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


def create_due_deligence_json(documents_as_sec_code, report_map, share_price_map):
    """
    株価の取得できた企業についてレポート結果をjson形式で返却
    """
    result_json = {}
    for sec_code in share_price_map:
        filer_name = documents_as_sec_code[sec_code][0].filer_name()
        print(sec_code, filer_name)
        stock_price = share_price_map[sec_code]
        print('株価', stock_price, '(円)')
        due_deligences = []
        for document in documents_as_sec_code[sec_code]:
            print(str(document.date()))
            if document.doc_id() not in report_map:
                due_deligence = {
                    'isError': True
                }
                due_deligences.append(due_deligence)
                continue
            report = report_map[document.doc_id()]
            underpriced = _underpriced(stock_price, report.value_per_share())
            # print('1株あたりの価値', report.value_per_share(), '(円)')
            # print('自己資本比率', report.capital_ratio())
            # print('安全圏', underpriced, '(%)')
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
            'stockPrice': stock_price,
            'due_deligences': due_deligences
        }
    return result_json


class ResultPresenter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def print(self, result: Dict):
        """
        分析結果を出力する
        """

# 以下はリファクタして消す予定。


def _underpriced(stock_price, value_per_share):
    """
    安全圏、割安度を確認
    """
    return round(100 * stock_price / value_per_share, 0)


def share_price_search(sec_code_list):
    share_price_map = {}
    for sec_code in sec_code_list:
        share_price = scrape_stock_price(sec_code)
        if share_price is not None:
            share_price_map[sec_code] = share_price
    return share_price_map


def scrape_stock_price(sec_code: str):
    try:
        value = scrape_value(sec_code)
        return to_int(value)
    except IndexError:
        logging.warning('現在の株価が取得できませんでした')
        return None
    except ValueError:
        logging.warning('現在の株価が存在しませんでした')
        return None
    except:
        logging.error('その他エラー')
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
