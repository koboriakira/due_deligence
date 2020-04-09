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
    target_date = sys.argv[2] if len(sys.argv) > 2 else None

    controller = dd_controller.DDController(
        from_date_str=target_date, print_result=True)
    controller.execute()


def pattern2():
    """
    指定された企業コードの分析を行います。
    先にpattern3を実行してデータの整備をする必要があります。
    """
    sec_code_list = sys.argv[2].split(',') if len(
        sys.argv) >= 3 else myconfig.TARGET_COMPANY_LIST

    controller = dd_controller.DDController(sec_code_list=sec_code_list)
    controller.execute()


def pattern3():
    """
    バッチ処理によって、指定期間の分析を行います。
    結果の出力は行いません。
    """
    from_date_str = sys.argv[2] if len(sys.argv) > 2 else None
    end_date_str = sys.argv[3] if len(sys.argv) > 3 else copy(from_date_str)

    controller = dd_controller.DDController(from_date_str=from_date_str,
                                            end_date_str=end_date_str, print_result=False)
    controller.execute()


if __name__ == '__main__':
    logging.basicConfig(filename='logfile/logger.log', level=logging.DEBUG)
    inject_config.init_injection()

    if len(sys.argv) == 1:
        pattern1()
    elif sys.argv[1] == '1':
        pattern1()
    elif sys.argv[1] == '2':
        pattern2()
    else:
        pattern3()
