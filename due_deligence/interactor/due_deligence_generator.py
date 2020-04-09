from datetime import date, timedelta
from copy import copy
import json
import inject

from due_deligence.util import calm_requests as requests

from . import analyze_financial_reports
from .due_deligence_requester import DueDeligenceRequester
from .company import Company
from .xbrl_repository import XbrlRepository


class DueDeligenceGenerator(DueDeligenceRequester):
  def __init__(self):
    self.xbrl_repository = inject.instance(XbrlRepository)

  def search(self, from_date: date, end_date: date):
    company_list = self._search_company_list(from_date, end_date)
    analyze_financial_reports.execute(company_list)

  def _search_company_list(self, from_date: date, end_date: date):
    """
    指定された期間にある企業の有価証券報告書のドキュメントリンク情報を取得
    """
    target_date = copy(from_date)

    result = []
    while from_date <= target_date and target_date <= end_date:
        company_list = self._search_company(target_date)
        result.extend(company_list)
        target_date = target_date + timedelta(days=1)

    return result

  def _search_company(self, target_date: date):
    company_list = self.xbrl_repository.search_by_date(target_date)
    if not company_list is None and len(company_list) > 0:
        return company_list

    list_url = self._get_list_url(str(target_date))
    response = requests.get(list_url)
    json_dict = json.loads(response.text)

    company_list = []
    for result in json_dict['results']:
        company = Company.construct_from_edinet(result, target_date)
        if company.is_financial_report():
            self.xbrl_repository.insert(company)
            company_list.append(company)

    return company_list

  def _get_list_url(self, date: str):
    # ex. https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=2020-03-17&type=2
    return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=' + date + '&type=2'
