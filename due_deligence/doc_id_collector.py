import calm_requests
import json
import logging
from datetime import date, timedelta
from typing import Dict, List

from company import Company


def search_company_list(from_date_str: str, end_date_str: str):
    """
    指定された期間にある企業の有価証券報告書のドキュメントリンク情報を取得
    """
    target_date = date.fromisoformat(from_date_str)
    from_date = date.fromisoformat(from_date_str)
    end_date = date.fromisoformat(end_date_str)

    result = []
    while from_date <= target_date and target_date <= end_date:
        company_list = search_company(target_date)
        result.extend(company_list)
        target_date = target_date + timedelta(days=1)

    return result


def search_company(target_date: date):
    list_url = get_list_url(str(target_date))
    response = calm_requests.get(list_url)
    json_dict = json.loads(response.text)

    company_list = []
    for result in json_dict['results']:
        company = Company(result)
        if company.is_target_financial_report():
            company_list.append(company)

    return company_list


def get_list_url(date: str):
    # ex. https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=2020-03-17&type=2
    return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=' + date + '&type=2'


if __name__ == '__main__':
    company_list = search_company_list('2020-03-17', '2020-03-17')
    for company in company_list:
        logging.debug(company.sec_code)
