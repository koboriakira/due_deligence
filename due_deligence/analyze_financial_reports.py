from analyzer import analyze
from typing import List
import sys
from company import Company


def execute(company_list: List[Company]):
    for company in company_list:
        print('*****', company.filer_name, company.sec_code, '*****')
        analyze(company)
        print('============================\n\n')


if __name__ == '__main__':
    data = {
        'docID': sys.argv[1],
        'filerName': 'テスト（パーク24）',
        'secCode': '99999'
    }
    company = Company(data)
    execute([company])
