import MySQLdb
from typing import List
from datetime import date
import logging

from due_deligence.adapter.document import Document, DocumentRepository
from due_deligence.deligence_model import DeligenceModel

INSERT_SQL = 'INSERT INTO document(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name) VALUES(%(doc_id)s, %(date)s, %(seq_number)s, %(edinet_code)s, %(sec_code)s, %(form_code)s, %(doc_type_code)s, %(filer_name)s)'
SELECT_SQL = 'SELECT doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name FROM document '
ORDER_SQL = ' ORDER BY sec_code, date DESC'

TEST_DATA = {
    'doc_id': 'XXXXXXX',
    'date': date.today(),
    'seq_number': 1111,
    'edinet_code': 'XXX9999',
    'sec_code': '9201',
    'form_code': '030000',
    'doc_type_code': '100',
    'filer_name': '日本航空',
}


class DocumentMysqlRepository(DocumentRepository):
    def __init__(self):
        # self.connection = MySQLdb.connect(db=param['db'], user=param['user'],
        #                    passwd=param['passwd'], charset=param['charset'])
        self._connection = MySQLdb.connect(db='db', user='admin',
                                           passwd='admin', charset='utf8mb4')

    def search_by_date(self, date: date) -> List[Document]:
        with self._connection.cursor() as c:
            select_sql = SELECT_SQL \
                + 'WHERE date = \'' \
                + str(date) + '\''
            c.execute(select_sql)
            results = c.fetchall()
            return self._generate_documents(results)

    def insert(self, document: Document):
        with self._connection.cursor() as c:
            try:
                c.execute(INSERT_SQL, document.to_entity())
                self._connection.commit()
                print('新しくデータを挿入しました', document.filer_name())
            except MySQLdb._exceptions.IntegrityError as e:
                logging.debug('データベースの登録に失敗しました', e)

    def search_by_sec_code(self, sec_code_list: List[str]) -> List[Document]:
        with self._connection.cursor() as c:
            format_strings = ','.join(['%s'] * len(sec_code_list))

            select_sql = SELECT_SQL \
                + 'WHERE ' \
                + '  sec_code in (' + format_strings + ')' \
                + '  AND form_code = \'030000\'' \
                + '  AND doc_type_code = \'120\'' \
                + ORDER_SQL
            c.execute(select_sql, tuple(sec_code_list))
            results = c.fetchall()
            return self._generate_documents(results)

    def _generate_documents(self, results) -> List[Document]:
        document_list = []
        for result in results:
            document = self._generate_document(result)
            document_list.append(document)

        return document_list

    def _generate_document(self, result) -> Document:
        doc_id = result[0]
        date = result[1]
        seq_number = result[2]
        edinet_code = result[3]
        sec_code = result[4]
        form_code = result[5]
        doc_type_code = result[6]
        filer_name = result[7]
        return Document(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name)
