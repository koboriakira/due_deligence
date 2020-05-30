from due_deligence.controller.dd_controller import ResultPresenter
from typing import Dict, List
from functools import reduce
import os
import requests
import logging

logger = logging.getLogger(__name__)

class ResultSlackPresenter(object):
    def print(self, result: Dict):
        logger.debug('print')
        slack_result = _SlackResult()
        for sec_code in result:
            texts:List[str] = []
            filer_name = result[sec_code]['filerName']
            share_price = str(result[sec_code]['stockPrice'])
            texts.append(f'*【{sec_code}】 {filer_name}...{share_price}円*\n\n')
            for due_deligence in result[sec_code]['due_deligences']:
                if due_deligence['isError']:
                    texts.append('* ファイルの解析に失敗しました。')
                value_per_share = due_deligence['valueParShare']
                capital_ratio = due_deligence['capitalRatio']
                underpriced = due_deligence['underpriced']
                texts.append(f'* 一株あたりの価値: {value_per_share}円\n')
                texts.append(f'* 自己資本比率: {capital_ratio}%\n')
                texts.append(f'* 安全圏: {underpriced}%\n')
            logger.debug('append')
            slack_result.append(texts)
        logger.debug(slack_result.blocks)
        slack_result.post()

class _SlackResult(object):
    BLOCK_TYPE = 'section'
    TEXT_TYPE = 'mrkdwn'

    def __init__(self, blocks=[]) -> None:
        self.blocks = blocks

    def append(self, texts:List[str]) -> None:
        block = {
            "type": self.BLOCK_TYPE,
            "text": {
                "type": self.TEXT_TYPE,
                "text": reduce(lambda text, cur: text + cur, texts)
            }
        }
        self.blocks.append(block)

    def post(self) -> None:
        logger.debug('post')
        json = {
            'blocks': self.blocks
        }
        url:str = os.environ.get('SLACK_INCOMING_WEBHOOK')
        requests.post(url, json=json)
