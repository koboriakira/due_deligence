from typing import List
import sys
from due_deligence.company import Company
from due_deligence.analyzer import analyze


def execute(company_list: List[Company]):
    for company in company_list:
        print('*****', company.to_str(), '*****')
        analyze(company)
        print('============================\n\n')
