import sys
import logging
from datetime import date
from copy import copy

from get_edinet import search_company_list, search_company_list_by_sec_code
import analyze_financial_reports
from config import TARGET_COMPANY_LIST, DETAIL, WAIT_TIME


def pattern1():
    logging.info('pattern1')
    """
    指定した日付に有価証券報告書を提出した企業について分析します。
    日付が指定されていない場合は実行当日とみなします。
    """
    if len(sys.argv) > 2:
        target_date = sys.argv[2]
    else:
        target_date = str(date.today())

    company_list = search_company_list(target_date, copy(target_date))
    analyze_financial_reports.execute(company_list)


def pattern2():
    """
    指定された企業コードの分析を行います。
    先にpattern3を実行してデータの整備をする必要があります。
    """
    logging.info('pattern2')
    DETAIL = True
    if len(sys.argv) < 3:
        logging.error('エラー 企業コードを指定してください')

    sec_code = sys.argv[2]
    company_list = search_company_list_by_sec_code(sec_code)
    analyze_financial_reports.execute(company_list)


def pattern3():
    """
    バッチ処理によって、指定期間の分析をゆっくり行います
    """
    logging.info('pattern3')
    WAIT_TIME = 5

    if len(sys.argv) > 2:
        from_date_str = sys.argv[2]
    else:
        from_date_str = str(date.today())

    if len(sys.argv) > 3:
        end_date_str = sys.argv[3]
    else:
        end_date_str = copy(from_date_str)

    company_list = search_company_list(from_date_str, end_date_str)
    analyze_financial_reports.execute(company_list)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error('エラー パターンを指定してください')

    if sys.argv[1] == '1':
        pattern1()
    elif sys.argv[1] == '2':
        pattern2()
    elif sys.argv[1] == '3':
        pattern3()

    # このあとYahoo株価から現時点の株価を取得したい
    # https://stocks.finance.yahoo.co.jp/stocks/detail/?code=7751.T
