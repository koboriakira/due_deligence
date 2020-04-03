import sys
from datetime import date
from copy import copy

from doc_id_collector import search_company_list
import analyze_financial_reports
from config import TARGET_COMPANY_LIST

if __name__ == '__main__':
    """
    指定された期間のうち、指定された企業の有価証券報告書を取得し、
    分析できるものは「1株あたりの株価」を出力する
    """
    if len(sys.argv) > 1:
        from_date_str = sys.argv[1]
    else:
        from_date_str = str(date.today())

    if len(sys.argv) > 2:
        end_date_str = sys.argv[2]
    else:
        end_date_str = copy(from_date_str)

    if len(sys.argv) > 3:
        TARGET_COMPANY_LIST = [sys.argv[3]]
    company_list = search_company_list(from_date_str, end_date_str)
    analyze_financial_reports.execute(company_list)

    # このあとYahoo株価から現時点の株価を取得したい
    # https://stocks.finance.yahoo.co.jp/stocks/detail/?code=7751.T
