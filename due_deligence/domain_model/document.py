from abc import ABCMeta, abstractmethod
from typing import List

TARGET_FORM_CODE_LIST = [
    '030000',  # 有価証券報告書
    # '043000',  # 四半期報告書
]

# 同じ030000でも350「大量保有報告書」の場合もあるので絞り込む
TARGET_DOC_TYPE_CODE = '120'


class Document(object):
    def __init__(self, doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name):
        self.__doc_id = doc_id
        self.__date = date
        self.__seq_number = seq_number
        self.__edinet_code = edinet_code
        self.__sec_code = sec_code
        self.__form_code = form_code
        self.__doc_type_code = doc_type_code
        self.__filer_name = filer_name

    def is_financial_report(self):
        return self.__form_code in TARGET_FORM_CODE_LIST and self.__doc_type_code == TARGET_DOC_TYPE_CODE and self.__sec_code is not None

    def generate_doc_url(self):
        # ex.) https://disclosure.edinet-fsa.go.jp/api/v1/documents/S100IA9D?type=1
        return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/' + self.__doc_id + '?type=1'

    def to_entity(self):
        return {
            'doc_id': self.__doc_id,
            'date': self.__date,
            'seq_number': self.__seq_number,
            'edinet_code': self.__edinet_code,
            'sec_code': self.__sec_code,
            'form_code': self.__form_code,
            'doc_type_code': self.__doc_type_code,
            'filer_name': self.__filer_name,
        }

    def doc_id(self):
        return self.__doc_id

    def filer_name(self):
        return self.__filer_name

    def sec_code(self):
        return self.__sec_code

    def date(self):
        return self.__date

    @classmethod
    def construct_from_edinet(cls, result, date):
        doc_id = result['docID']
        seq_number = result['seqNumber']
        edinet_code = result['edinetCode']
        sec_code = None
        if type(result['secCode']) is str:
            sec_code = result['secCode'][0:len(result['secCode']) - 1]
        form_code = result['formCode']
        doc_type_code = result['docTypeCode']
        filer_name = result['filerName']
        return Document(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name)


class DocumentService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self, start_date, end_date):
        raise NotImplementedError

    @abstractmethod
    def search_by_sec_code(self, sec_code_list: List[str]):
        raise NotImplementedError
