import MySQLdb
import logging
from typing import List
from datetime import date

from due_deligence.domain_model.deligence import Deligence
from due_deligence.adapter.deligence import ReportRepository

INSERT_SQL = 'INSERT INTO report(' + \
    'doc_id, value_per_share, capital_ratio, current_year_operating_income, prior_1year_operating_income, current_year_current_assets, current_year_investments_and_other_assets, current_year_current_liabilities, current_year_noncurrent_liabilities, current_year_net_assets, current_year_total_number_of_issued_shares, updated_at) ' + \
    'VALUES(%(doc_id)s, %(value_per_share)s, %(capital_ratio)s, %(current_year_operating_income)s, %(prior_1year_operating_income)s, %(current_year_current_assets)s, %(current_year_investments_and_other_assets)s, %(current_year_current_liabilities)s, %(current_year_noncurrent_liabilities)s, %(current_year_net_assets)s, %(current_year_total_number_of_issued_shares)s, %(updated_at)s )'

SELECT_SQL_WHERE_DOC_ID = 'SELECT ' \
    + 'doc_id, value_per_share, capital_ratio, current_year_operating_income, prior_1year_operating_income, current_year_current_assets, current_year_investments_and_other_assets, current_year_current_liabilities, current_year_noncurrent_liabilities, current_year_net_assets, current_year_total_number_of_issued_shares, updated_at ' \
    + 'FROM report ' \
    + 'WHERE doc_id = %(doc_id)s'

class ReportMysqlRepository(ReportRepository):
  def __init__(self):
    self._connection = conn = MySQLdb.connect(db='db', user='admin',
                      passwd='admin', charset='utf8mb4')

  def find(self, doc_id):
    with self._connection.cursor() as c:
      c.execute(SELECT_SQL_WHERE_DOC_ID, {'doc_id': doc_id})
      result = c.fetchone()
      if result is None:
          return None
      return self._to_entity(result)


  def insert(self, deligence: Deligence):
    with self._connection.cursor() as c:
      try:
        c.execute(INSERT_SQL, deligence.to_dto())
        self._connection.commit()
        logging.info('新しくデータを挿入しました', deligence.doc_id)
      except MySQLdb._exceptions.IntegrityError as e:
        logging.warn('データベースの登録に失敗しました', e)

  def _to_entity(self, result):
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
    return Deligence(data)
