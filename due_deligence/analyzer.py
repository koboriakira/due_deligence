import logging
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser

from download_file import download_file
from get_xbrl import get_xbrl
import deligence_model
from company import Company
from scrape_stock_price import scrape_stock_price
import deligence_repository

ITEMS = {
    '当期営業利益': ['jppfs_cor:OperatingIncome', 'CurrentYearDuration'],
    '前期営業利益': ['jppfs_cor:OperatingIncome', 'Prior1YearDuration'],
    '当期流動資産合計': ['jppfs_cor:CurrentAssets', 'CurrentYearInstant'],
    '当期その他の資産合計': ['jppfs_cor:InvestmentsAndOtherAssets', 'CurrentYearInstant'],
    '当期流動負債合計': ['jppfs_cor:CurrentLiabilities', 'CurrentYearInstant'],
    '当期固定負債合計': ['jppfs_cor:NoncurrentLiabilities', 'CurrentYearInstant'],
    '当期純資産合計': ['jppfs_cor:NetAssets', 'CurrentYearInstant'],
    '当期発行済株式総数': ['jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults', 'CurrentYearInstant_NonConsolidatedMember'],
}

ITEMS_2 = {
    '': ['jppfs_cor:CurrentAssets', 'Prior1YearInstant']
}


def analyze(company: Company):
    deligence = get_deligence(company)
    if deligence is None:
        return

    print('1株あたりの価値', deligence.value_per_share(), '(円)')

    stock_price = scrape_stock_price(company)
    if not stock_price is None:
        print('株価', stock_price, '(円)')
        print('安全圏', underpriced(stock_price,
                                 deligence.value_per_share()), '(%)')


def get_deligence(company: Company):
    deligence = deligence_repository.find(company.doc_id)
    if not deligence is None:
        return deligence

    detail_url = company.generate_doc_url()

    # XBRLの取得
    path = download_file(detail_url)
    if not path:
        logging.error('エラー！ ファイルが取得または開くことができませんでした')
        return None

    xbrl_path = get_xbrl(path)
    parser = EdinetXbrlParser()
    edinet_obj = parser.parse_file(xbrl_path)

    # XBRLの解析
    xbrl_dict = get_value_dict(edinet_obj)
    if not xbrl_dict:
        logging.error('エラー！ XBRLの解析ができませんでした')
        return None

    deligence = deligence_model.contruct_by_xbrl_dict(
        company.doc_id, xbrl_dict)
    deligence_repository.insert(deligence)
    return deligence


def get_value_dict(edinet_obj):
    try:
        value_dict = {}
        for item_name in ITEMS:
            key = ITEMS[item_name][0]
            context_ref = ITEMS[item_name][1]
            logging.debug(key, context_ref)
            item_value = edinet_obj.get_data_by_context_ref(
                key, context_ref).get_value()
            if item_value is None:
                logging.warning('取得できない項目があります:', item_name)
                return False
            value_dict[item_name] = item_value
        return value_dict
    except AttributeError as e:
        return False


def underpriced(stock_price, value_per_share):
    """
    安全圏、割安度を確認
    """
    return round(100 * stock_price / value_per_share, 0)
