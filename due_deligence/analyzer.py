import logging
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser

from download_file import download_file
from get_xbrl import get_xbrl
from deligence_model import DeligenceModel
from company import Company

ITEMS = {
    '当期営業利益': ['jppfs_cor:OperatingIncome', 'CurrentYearDuration'],
    '前期営業利益': ['jppfs_cor:OperatingIncome', 'Prior1YearDuration'],
    '当期流動資産合計': ['jppfs_cor:CurrentAssets', 'CurrentYearInstant'],
    '当期その他の資産合計': ['jppfs_cor:InvestmentsAndOtherAssets', 'CurrentYearInstant'],
    '当期流動負債合計': ['jppfs_cor:CurrentLiabilities', 'CurrentYearInstant'],
    '当期固定負債合計': ['jppfs_cor:NoncurrentLiabilities', 'CurrentYearInstant'],
    '当期発行済株式総数': ['jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults', 'CurrentYearInstant_NonConsolidatedMember']
}

ITEMS_2 = {
    '': ['jppfs_cor:CurrentAssets', 'Prior1YearInstant']
}


def analyze(company: Company):
    detail_url = company.generate_doc_url()
    print(detail_url)

    # XBRLの取得
    path = download_file(detail_url)
    if not path:
        logging.error('エラー！ ファイルが取得または開くことができませんでした')

    xbrl_path = get_xbrl(path)
    parser = EdinetXbrlParser()
    edinet_obj = parser.parse_file(xbrl_path)

    # XBRLの解析
    value_dict = get_value_dict(edinet_obj)
    if not value_dict:
        logging.error('エラー！ XBRLの解析ができませんでした')
        return

    deligence_model = DeligenceModel(value_dict)
    print('1株あたりの価値', deligence_model.get_value_per_share(), '(円)')


def get_value_dict(edinet_obj):
    try:
        value_dict = {}
        for item_name in ITEMS:
            key = ITEMS[item_name][0]
            context_ref = ITEMS[item_name][1]
            logging.debug(key, context_ref)
            item_value = edinet_obj.get_data_by_context_ref(
                key, context_ref).get_value()
            value_dict[item_name] = item_value
        return value_dict
    except AttributeError as e:
        return False
