
import MySQLdb
from typing import List
from datetime import date

from due_deligence.company import Company
from due_deligence.deligence_model import DeligenceModel

INSERT_SQL = 'INSERT INTO company(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name) VALUES(%(doc_id)s, %(date)s, %(seq_number)s, %(edinet_code)s, %(sec_code)s, %(form_code)s, %(doc_type_code)s, %(filer_name)s)'
SELECT_SQL = 'SELECT doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name FROM company '
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

conn = MySQLdb.connect(db='db', user='admin',
                       passwd='admin', charset='utf8mb4')


def find(doc_id: str):
    c = conn.cursor()
    select_sql = SELECT_SQL + 'WHERE doc_id = \'' + doc_id + '\''
    c.execute(select_sql)
    result = c.fetchone()

    if result is None:
        c.close()
        return None

    return generate_company(result)

def search_company_list_by_sec_code(sec_code_list: List[str]):
    print(sec_code_list)
    c = conn.cursor()
    format_strings = ','.join(['%s'] * len(sec_code_list))
    print(format_strings)

    select_sql = SELECT_SQL \
        + 'WHERE ' \
        + '  sec_code in (' + format_strings + ')' \
        + '  AND form_code = \'030000\'' \
        + '  AND doc_type_code = \'120\'' \
        + ORDER_SQL
    c.execute(select_sql, tuple(sec_code_list))
    results = c.fetchall()

    print(len(results))

    company_list = []
    for result in results:
        company = generate_company(result)
        print(company.doc_id)
        company_list.append(company)
    c.close()
    print(company_list)
    return company_list
