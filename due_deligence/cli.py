import sys
import logging
from datetime import date
from copy import copy
import inject
import argparse

from datetime import date
from due_deligence.filtering.result_filter import ResultFilter
from due_deligence.filtering.result_underpriced_filter import ResultUnderpricedFilter
from due_deligence.controller import dd_controller
from due_deligence.myconfig import myconfig, inject_config

# CUIで `duedeli` を実行したときの最初の入口がこれ


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--date', help='YYYY-MM-DD形式で指定。指定された日付に共有された有価証券報告書を解析します。', type=str, default='')
    parser.add_argument(
        '--output', help='結果の出力先を指定します。\nCSV出力またはjson出力の場合に有効になります。', type=str, default='')
    parser.add_argument(
        '--format', help='結果の出力形式を指定します。CSV出力、json出力から選択できます。\n指定しない場合は標準出力されます。', choices=['csv', 'json'], default='screen')
    parser.add_argument(
        '--underpriced', help='指定した割安度より割安な企業に絞り込みます', type=int, default=-1)
    parser.add_argument('--debug', help='開発者モード', type=bool, default=False)
    args = parser.parse_args()

    # ログ設定
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(handlers=[logging.NullHandler()])

    # 依存制御の設定
    inject_config.init_injection(
        output_path=args.output, format_type=args.format, is_cli=True)

    # 処理の実行
    target_date_str = args.date if len(args.date) > 0 else str(date.today())
    filters = []
    if args.underpriced > 0:
        filters.append(ResultUnderpricedFilter(args.underpriced))
    try:
        target_date = date.fromisoformat(target_date_str)
        controller = dd_controller.DDController(
            from_date=target_date, filters=filters)
        result = controller.execute()

        presenter = inject.instance(dd_controller.ResultPresenter)
        presenter.print(result)
    except ValueError as ve:
        logger = logging.getLogger(__name__)
        logger.exception('例外を検出しました。 %s', ve)
        print('引数の指定が誤っています。')
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception('例外を検出しました。 %s', e)
        print('処理に失敗しました。')
