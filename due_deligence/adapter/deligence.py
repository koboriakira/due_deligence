from abc import ABCMeta, abstractmethod
import inject
from logging import getLogger
import traceback
from typing import List, Union, Dict
from tqdm import tqdm

from due_deligence.domain_model.deligence import Deligence, DeligenceService
from due_deligence.util.progress_presenter import ProgressPresenter

logger = getLogger(__name__)

ITEMS = {
    '当期営業利益': [['jppfs_cor:OperatingIncome', 'CurrentYearDuration'], ['jppfs_cor:OperatingIncome', 'CurrentYearDuration_NonConsolidatedMember']],
    '前期営業利益': [['jppfs_cor:OperatingIncome', 'Prior1YearDuration'], ['jppfs_cor:OperatingIncome', 'Prior1YearDuration_NonConsolidatedMember']],
    '当期流動資産合計': [['jppfs_cor:CurrentAssets', 'CurrentYearInstant'], ['jppfs_cor:CurrentAssets', 'CurrentYearInstant_NonConsolidatedMember']],
    '当期その他の資産合計': [['jppfs_cor:InvestmentsAndOtherAssets', 'CurrentYearInstant'], ['jppfs_cor:InvestmentsAndOtherAssets', 'CurrentYearInstant_NonConsolidatedMember']],
    '当期流動負債合計': [['jppfs_cor:CurrentLiabilities', 'CurrentYearInstant'], ['jppfs_cor:CurrentLiabilities', 'CurrentYearInstant_NonConsolidatedMember']],
    '当期固定負債合計': [['jppfs_cor:NoncurrentLiabilities', 'CurrentYearInstant'], ['jppfs_cor:NoncurrentLiabilities', 'CurrentYearInstant_NonConsolidatedMember']],
    '当期純資産合計': [['jppfs_cor:NetAssets', 'CurrentYearInstant'], ['jppfs_cor:NetAssets', 'CurrentYearInstant_NonConsolidatedMember']],
    '当期発行済株式総数': [['jpcrp_cor:TotalNumberOfIssuedSharesSummaryOfBusinessResults', 'CurrentYearInstant_NonConsolidatedMember'], ['jpcrp030000-asr_E35323-000:TotalNumberOfIssuedSharesCommonStockSummaryOfBusinessResults', 'CurrentYearInstant_NonConsolidatedMember']],
}


class SimpleDeligenceService(DeligenceService):
    def __init__(self):
        self._downloader = inject.instance(XbrlDownloader)
        self._progress_presenter = inject.instance(ProgressPresenter)

    def search(self, doc_id_list: List[str]) -> Dict:
        if len(doc_id_list) == 0:
            self._progress_presenter.print('- 解析対象のファイルが存在しませんでした')
            return {}
        self._progress_presenter.print('- ファイルの解析を行います')
        deligence_map = {}
        for i in self._progress_presenter.wrap_tqdm(range(len(doc_id_list))):
            doc_id = doc_id_list[i]
            deligence = self._get_deligence(doc_id)
            if deligence is not None:
                deligence_map[deligence.doc_id] = deligence
        return deligence_map

    def _get_deligence(self, doc_id: str):
        edinet_obj = self._downloader.get(doc_id)

        # XBRLの解析
        xbrl_dict = edinet_obj.get_value_dict()
        if not xbrl_dict:
            logger.error('エラー！ XBRLの解析ができませんでした doc_id:%s' % doc_id)
            return None

        deligence = Deligence.contruct_by_xbrl_dict(doc_id, xbrl_dict)
        return deligence


class EdinetObjWrapper:
    def __init__(self, edinet_obj):
        self._edinet_obj = edinet_obj

    def get_value_dict(self):
        try:
            value_dict = {}
            for item_name in ITEMS:
                key_and_ref_list = ITEMS[item_name]
                item_value = self._get_item_value(key_and_ref_list)
                if item_value is None:
                    # 当期固定負債合計は存在しない場合がある
                    if item_name == '当期固定負債合計':
                        value_dict[item_name] = 0
                        continue
                    logger.error('取得できない項目がありました: %s' % item_name)
                    return False
                value_dict[item_name] = item_value
            return value_dict
        except AttributeError as e:
            logger.exception('例外が発生しました。 %s', e)
            return False

    def _get_item_value(self, key_and_ref_list) -> Union[str, int]:
        for key_and_ref in key_and_ref_list:
            key = key_and_ref[0]
            context_ref = key_and_ref[1]
            data = self._edinet_obj.get_data_by_context_ref(key, context_ref)
            if data is not None:
                return data.get_value() if data.get_value() is not None else 0
        return None


class XbrlDownloader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, doc_id) -> EdinetObjWrapper:
        """
        指定されたdocIDをもとにxbrlファイルをダウンロードして、
        その中身をXbrlEdinetParserでparseしたものを返却する
        """
        raise NotImplementedError
