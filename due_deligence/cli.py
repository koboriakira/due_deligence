import sys
import logging
from datetime import date
from copy import copy
import inject

from due_deligence.controller import dd_controller
from due_deligence.myconfig import myconfig, inject_config

# pip install でduedeliコマンドが使えるようになったとき、
# duedeliコマンド


def main():
    logging.basicConfig(level=logging.ERROR)
    logging.info('pattern1')
    """
    指定した日付に有価証券報告書を提出した企業について分析します。
    日付が指定されていない場合は実行当日とみなします。
    """
    inject_config.init_injection(today_recommend=True)
    target_date = sys.argv[2] if len(sys.argv) > 2 else None

    controller = dd_controller.DDController(
        from_date_str=target_date, print_result=True)
    controller.execute()
