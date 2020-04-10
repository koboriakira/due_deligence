from due_deligence.adapter.deligence import Deligence, EdinetObjWrapper
from edinet_xbrl.edinet_xbrl_parser import EdinetXbrlParser
import sys


def test_edinet_obj_wrapper():
    assert get_value_dict('S100IC6Q')
    assert get_value_dict('S100FRGF')


def get_value_dict(filename: str):
    parser = EdinetXbrlParser()
    suite = EdinetObjWrapper(parser.parse_file(
        'tests/adapter/%s.xbrl' % filename))
    return suite.get_value_dict()
