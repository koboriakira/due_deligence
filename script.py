import sys
import logging
from datetime import date
from copy import copy
import inject

from due_deligence.controller import dd_controller
from due_deligence.myconfig import myconfig, inject_config


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

    dd_controller.pattern1(target_date)


def pattern2():
    """
    指定された企業コードの分析を行います。
    先にpattern3を実行してデータの整備をする必要があります。
    """
    logging.info('pattern2')

    sec_code_list = myconfig.TARGET_COMPANY_LIST
    if len(sys.argv) >= 3:
        sec_code_list = sys.argv[2].split(',')

    dd_controller.pattern2(sec_code_list)


def pattern3():
    """
    バッチ処理によって、指定期間の分析をゆっくり行います
    """
    logging.info('pattern3')

    if len(sys.argv) > 2:
        from_date_str = sys.argv[2]
    else:
        from_date_str = str(date.today())

    if len(sys.argv) > 3:
        end_date_str = sys.argv[3]
    else:
        end_date_str = copy(from_date_str)

    dd_controller.pattern3(from_date_str, end_date_str)


if __name__ == '__main__':
    logging.basicConfig(filename='logfile/logger.log', level=logging.DEBUG)
    inject_config.init_injection()

    if len(sys.argv) == 1:
        pattern1()
    elif sys.argv[1] == '1':
        pattern1()
    elif sys.argv[1] == '2':
        pattern2()
    elif sys.argv[1] == '3':
        pattern3()
