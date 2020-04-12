from due_deligence.adapter.deligence import Deligence, EdinetObjWrapper
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import sys


def test_edinet_obj_wrapper():
    # https://disclosure.edinet-fsa.go.jp/api/v1/documents/S100FYQX?type=1
    assert get_value_dict('S100IC6Q')
    assert get_value_dict('S100FRGF')
    assert get_value_dict('S100ICAI')
    assert get_value_dict('S100I8Y1')
    assert get_value_dict('S100IB07')


def test_not_have_operating_income():
    """
    営業利益がない場合（ライフネット生命） -> S100FYQX
    たぶんこれもそう
    S100FZYB
    S100FZDC
    S100G10A
    S100G1CG
    S100G138
    S100FZSL
    """
    pass


def test_total_number_of_issued_shares():
    """
    TotalNumberOfIssuedSharesSummaryOfBusinessResults
    ERROR:due_deligence.adapter.deligence:取得できない項目がありました: 当期発行済株式総数
    ERROR:due_deligence.adapter.deligence:エラー！ XBRLの解析ができませんでした doc_id:S100G3GR
    """
    pass


def get_value_dict(filename: str):
    parser = EdinetXbrlParser()
    suite = EdinetObjWrapper(parser.parse_file(
        'tests/adapter/%s.xbrl' % filename))
    return suite.get_value_dict()
