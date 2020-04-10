from abc import ABCMeta, abstractmethod
from datetime import date, timedelta
from copy import copy
import json
import inject
from typing import List
from tqdm import tqdm

from due_deligence.domain_model.document import Document, DocumentService
from due_deligence.util import calm_requests as requests


class SimpleDocumentService(DocumentService):

    def __init__(self):
        self._repo = inject.instance(DocumentRepository)

    def search(self, from_date: date, end_date: date) -> List[Document]:
        """
        指定された期間にある企業の有価証券報告書のドキュメントリンク情報を取得
        """
        print('- xbrlファイルの一覧を取得します。')
        target_date = copy(from_date)

        result = []
        dt = from_date - end_date
        for i in tqdm(range(dt.days + 1)):
            # while from_date <= target_date and target_date <= end_date:
            document_list = self._search_document(target_date)
            result.extend(document_list)
            target_date = target_date + timedelta(days=1)

        return result

    def search_by_sec_code(self, sec_code_list: List[str]) -> List[Document]:
        document_list = self._repo.search_by_sec_code(sec_code_list)
        if document_list is None:
            raise AttributeError
        return document_list

    def _search_document(self, target_date: date) -> List[Document]:
        document_list = self._repo.search_by_date(target_date)
        if document_list is not None and len(document_list) > 0:
            return document_list

        list_url = self._get_list_url(str(target_date))
        response = requests.get(list_url)
        json_dict = json.loads(response.text)

        document_list = []
        for result in json_dict['results']:
            document = Document.construct_from_edinet(result, target_date)
            if document.is_financial_report():
                self._repo.insert(document)
                document_list.append(document)

        return document_list

    def _get_list_url(self, date: str):
        # ex. https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=2020-03-17&type=2
        return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=' + date + '&type=2'


class DocumentRepository(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_by_date(self, target_date: date) -> List[Document]:
        raise NotImplementedError

    @abstractmethod
    def insert(self, document: Document):
        raise NotImplementedError

    @abstractmethod
    def search_by_sec_code(self, sec_code_list: List[str]) -> List[Document]:
        raise NotImplementedError
