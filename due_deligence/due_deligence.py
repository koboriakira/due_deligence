import logging
from datetime import date
import inject
from typing import Dict, Optional

from due_deligence.controller import dd_controller
from due_deligence.myconfig import myconfig, inject_config


class DueDeligence:
    def __init__(self, target_date_str: str = '', debug: bool = False):
        try:
            if target_date_str:
                self._target_date = date.fromisoformat(target_date_str)
            else:
                self._target_date = date.today()
        except ValueError as ve:
            logger = logging.getLogger(__name__)
            logger.exception('例外を検出しました。 %s', ve)
        # ログ設定
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(handlers=[logging.NullHandler()])

    def execute(self):
        # 依存制御の設定
        inject_config.init_injection()

        # 処理の実行
        try:
            controller = dd_controller.DDController(self._target_date)
            return controller.execute()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception('例外を検出しました。 %s', e)
            return None
