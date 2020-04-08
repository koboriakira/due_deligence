import json
import logging
from datetime import date, timedelta
from typing import Dict, List

from due_deligence import calm_requests
from due_deligence.company import Company
from due_deligence import company_repository


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


def search_company_list_by_sec_code(sec_code_list: List[str]):
    """
    指定された企業コードの有価証券報告書をDBから調べます。
    もし見つからない場合は、まずDBへの保存を先にやってください。
    """
    return company_repository.search_company_list_by_sec_code(sec_code_list)


def search_company(target_date: date):
    company_list = company_repository.search_by_date(target_date)
    if not company_list is None and len(company_list) > 0:
        return company_list

    list_url = get_list_url(str(target_date))
    response = calm_requests.get(list_url)
    json_dict = json.loads(response.text)

    company_list = []
    for result in json_dict['results']:
        company = generate_company(result, target_date)
        if company.is_financial_report():
            company_repository.insert(company)
            company_list.append(company)

    return company_list


def generate_company(result, date):
    doc_id = result['docID']
    seq_number = result['seqNumber']
    edinet_code = result['edinetCode']
    sec_code = None
    if type(result['secCode']) is str:
        sec_code = result['secCode'][0:len(result['secCode']) - 1]
    form_code = result['formCode']
    doc_type_code = result['docTypeCode']
    filer_name = result['filerName']
    return Company(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name)


def get_list_url(date: str):
    # ex. https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=2020-03-17&type=2
    return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date=' + date + '&type=2'


if __name__ == '__main__':
    company_list = search_company_list('2020-03-17', '2020-03-17')
    for company in company_list:
        logging.debug(company.sec_code)
