
import MySQLdb
from company import Company
from typing import List
from datetime import date
from deligence_model import DeligenceModel

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


def search_by_date(date):
    c = conn.cursor()
    select_sql = SELECT_SQL + 'WHERE date = \'' + str(date) + '\''
    c.execute(select_sql)
    results = c.fetchall()

    company_list = []
    for result in results:
        company = generate_company(result)
        company_list.append(company)
    c.close()
    return company_list


def search_company_list_by_sec_code(sec_code: str):
    print(sec_code)
    c = conn.cursor()
    select_sql = SELECT_SQL + 'WHERE sec_code = \'' + \
        sec_code + '\' AND form_code = \'030000\' AND doc_type_code = \'120\'' + ORDER_SQL
    c.execute(select_sql)
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


def generate_company(result):
    doc_id = result[0]
    date = result[1]
    seq_number = result[2]
    edinet_code = result[3]
    sec_code = result[4]
    form_code = result[5]
    doc_type_code = result[6]
    filer_name = result[7]
    return Company(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name)

# def search_stores(urls: List[str]) -> List[Store]:
#     c = conn.cursor()
#     format_strings = ','.join(['%s'] * len(urls))
#     query = "SELECT * FROM stores WHERE url in (%s)" % format_strings
#     result_amount = c.execute(query, tuple(urls))
#     if result_amount == 0:
#         c.close()
#         return []

#     stores = []
#     for result in c.fetchall():
#         name = result[1]
#         rate = result[2]
#         address = result[3]
#         address_image_url = result[4]
#         url = result[5]
#         store = Store(name, rate, address, address_image_url, url)
#         stores.append(store)

#     c.close()
#     return stores


def insert(company: Company):
    if not find(company.doc_id) is None:
        return
    c = conn.cursor()
    print('新しくデータを挿入します', company.filer_name)
    c.execute(INSERT_SQL, company.to_entity())
    conn.commit()
    c.close()


def update_deligence(company: Company, deligence_model: DeligenceModel):
    c = conn.cursor()
    update_sql = 'UPDATE xbrl SET value_per_share = %(value_per_share)s, capital_ratio = %(capital_ratio)s WHERE doc_id = %(doc_id)s'
    params = {
        'value_per_share': deligence_model.value_per_share(),
        'capital_ratio': deligence_model.capital_ratio(),
        'doc_id': company.doc_id
    }
    conn.commit()
    c.close()


def close_db():
    conn.close()
