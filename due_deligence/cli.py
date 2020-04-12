import sys
import logging
from datetime import date
from copy import copy
import inject
import argparse
from typing import List, Tuple

from due_deligence.filtering.result_filter import ResultFilter
from due_deligence.filtering.result_underpriced_filter import ResultUnderpricedFilter
from due_deligence.filtering.result_capital_ratio_filter import ResultCapitalRatioFilter
from due_deligence.filtering.result_stock_price_filter import ResultStockPriceFilter
from due_deligence.controller import dd_controller
from due_deligence.myconfig import myconfig, inject_config

# CUIで `duedeli` を実行したときの最初の入口がこれ


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--date', help='YYYY-MM-DDまたはYYYY-MM-DD_YYYY-MM-DD形式で指定。指定された日付または期間に提出された有価証券報告書を解析します。', type=str, default='')
    parser.add_argument(
        '--output', help='結果の出力先を指定します。\nCSV出力またはjson出力の場合に有効になります。', type=str, default='')
    parser.add_argument(
        '--format', help='結果の出力形式を指定します。CSV出力、json出力から選択できます。\n指定しない場合は標準出力されます。', choices=['csv', 'json'], default='screen')
    parser.add_argument(
        '--underpriced', help='指定した割安度より割安な企業に絞り込みます', type=int, default=-1)
    parser.add_argument(
        '--capital', help='自己資本比率が指定した割合より高い企業に絞り込みます', type=int, default=-1)
    parser.add_argument(
        '--price', help='指定した値より安い株価の企業に絞り込みます', type=int, default=-1)
    parser.add_argument(
        '--cache', help='スクレイピング結果をキャッシュします。容量が大きくなるため非推奨です', type=bool, default=False)
    parser.add_argument('--debug', help='開発者モード', type=bool, default=False)
    args = parser.parse_args()

    # ログ設定
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(handlers=[logging.NullHandler()])

    # 依存制御の設定
    inject_config.init_injection(
        output_path=args.output, format_type=args.format, is_cli=True, is_cache=args.cache)

    # 処理の実行
    try:
        target_dates = extract_date(args.date)
        filters = prepare_filters(args.underpriced, args.capital, args.price)
        controller = dd_controller.DDController(
            from_date=target_dates[0], end_date=target_dates[1], filters=filters)
        result = controller.execute()

        presenter = inject.instance(dd_controller.ResultPresenter)
        presenter.print(result)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception('例外を検出しました。 %s', e)
        print('処理に失敗しました。')


def extract_date(val: str) -> Tuple[date, date]:
    if len(val) == 0:
        from_date = date.today()
        end_date = copy(from_date)
        return from_date, end_date
    if val[10:11] == '_':
        from_date = date.fromisoformat(val[0:10])
        end_date = date.fromisoformat(val[11:22])
        return from_date, end_date
    from_date = date.fromisoformat(val)
    end_date = copy(from_date)
    return from_date, end_date


def prepare_filters(underpriced: int, capital: int, price: int) -> List[ResultFilter]:
    filters = []
    if underpriced > 0:
        filters.append(ResultUnderpricedFilter(underpriced))
    if capital > 0:
        filters.append(ResultCapitalRatioFilter(capital))
    if price > 0:
        filters.append(ResultStockPriceFilter(price))
    return filters
