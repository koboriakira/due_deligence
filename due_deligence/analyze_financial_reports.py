from analyzer import analyze
from typing import List
import sys
from company import Company


def execute(company_list: List[Company]):
    for company in company_list:
        print('*****', company.to_str(), '*****')
        analyze(company)
        print('============================\n\n')
