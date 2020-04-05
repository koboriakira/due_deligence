import MySQLdb
import logging
from typing import List
from datetime import date
from deligence_model import DeligenceModel

conn = MySQLdb.connect(db='db', user='admin',
                       passwd='admin', charset='utf8mb4')


INSERT_SQL = 'INSERT INTO deligence(' + \
    'doc_id, value_per_share, capital_ratio, current_year_operating_income, prior_1year_operating_income, current_year_current_assets, current_year_investments_and_other_assets, current_year_current_liabilities, current_year_noncurrent_liabilities, current_year_net_assets, current_year_total_number_of_issued_shares, updated_at) ' + \
    'VALUES(%(doc_id)s, %(value_per_share)s, %(capital_ratio)s, %(current_year_operating_income)s, %(prior_1year_operating_income)s, %(current_year_current_assets)s, %(current_year_investments_and_other_assets)s, %(current_year_current_liabilities)s, %(current_year_noncurrent_liabilities)s, %(current_year_net_assets)s, %(current_year_total_number_of_issued_shares)s, %(updated_at)s )'

SELECT_SQL_WHERE_DOC_ID = 'SELECT ' \
    + 'doc_id, value_per_share, capital_ratio, current_year_operating_income, prior_1year_operating_income, current_year_current_assets, current_year_investments_and_other_assets, current_year_current_liabilities, current_year_noncurrent_liabilities, current_year_net_assets, current_year_total_number_of_issued_shares, updated_at ' \
    + 'FROM deligence ' \
    + 'WHERE doc_id = %(doc_id)s'


def find(doc_id: str):
    c = conn.cursor()
    c.execute(SELECT_SQL_WHERE_DOC_ID, {'doc_id': doc_id})
    result = c.fetchone()

    if result is None:
        c.close()
        return None

    return to_entity(result)


def to_entity(result):
    data = {
        'doc_id': result[0],
        'current_year_operating_income': result[3],
        'prior_1year_operating_income': result[4],
        'current_year_current_assets': result[5],
        'current_year_investments_and_other_assets': result[6],
        'current_year_current_liabilities': result[7],
        'current_year_noncurrent_liabilities': result[8],
        'current_year_net_assets': result[9],
        'current_year_total_number_of_issued_shares': result[10],
    }
    return DeligenceModel(data)


def insert(deligence_model: DeligenceModel):
    if not find(deligence_model.doc_id) is None:
        return
    c = conn.cursor()
    logging.info('新しくデータを挿入します', deligence_model.doc_id)
    c.execute(INSERT_SQL, deligence_model.to_dto())
    conn.commit()
    c.close()


def close_db():
    conn.close()


TEST_DATA = {
    'doc_id': 'TEST',
    'value_per_share': 100,
    'capital_ratio': 100,
    'current_year_operating_income': 100,
    'prior_1year_operating_income': 100,
    'current_year_current_assets': 100,
    'current_year_investments_and_other_assets': 100,
    'current_year_current_liabilities': 100,
    'current_year_noncurrent_liabilities': 100,
    'current_year_net_assets': 100,
    'current_year_total_number_of_issued_shares': 100,
    'updated_at': date.today(),
}
