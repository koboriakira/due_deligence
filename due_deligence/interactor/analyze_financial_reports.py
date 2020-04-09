from typing import List
import sys
from due_deligence.interactor.company import Company
from due_deligence.interactor import analyzer


def execute(company_list: List[Company]):
    for company in company_list:
        print('*****', company.to_str(), '*****')
        analyzer.analyze(company)
        print('============================\n\n')
