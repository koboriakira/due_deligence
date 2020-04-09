import json
import logging
from datetime import date, timedelta
from typing import Dict, List

from due_deligence.interactor.company import Company



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
