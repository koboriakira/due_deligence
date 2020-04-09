from abc import ABCMeta, abstractmethod
import inject
import logging

from due_deligence.domain_model.deligence import Deligence, DeligenceService

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

class SimpleDeligenceService(DeligenceService):
  def __init__(self):
    self._repo = inject.instance(ReportRepository)
    self._downloader = inject.instance(XbrlDownloader)

  def search(self, doc_id_list):
    deligence_map = {}
    for doc_id in doc_id_list:
      deligence = self._get_deligence(doc_id)
      if deligence is not None:
        deligence_map[deligence.doc_id] = deligence
    return deligence_map

  def _get_deligence(self, doc_id):
    # あとでリポジトリ.findを入れる
    deligence = self._repo.find(doc_id)
    if deligence is not None:
      return deligence

    edinet_obj = self._downloader.get(doc_id)

    # XBRLの解析
    xbrl_dict = self._get_value_dict(edinet_obj)
    if not xbrl_dict:
        logging.error('エラー！ XBRLの解析ができませんでした')
        return None

    deligence = Deligence.contruct_by_xbrl_dict(doc_id, xbrl_dict)
    self._repo.insert(deligence)
    # deligence_repository.insert(deligence)
    return deligence

  def _get_value_dict(self, edinet_obj):
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

class XbrlDownloader(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def get(self, doc_id):
    """
    指定されたdocIDをもとにxbrlファイルをダウンロードして、
    その中身をXbrlEdinetParserでparseしたものを返却する
    """
    raise NotImplementedError

class ReportRepository(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def find(self, doc_id):
    """
    指定されたdoc_idに一致するdeligenceテーブルのレコードを返す
    """
    raise NotImplementedError

  @abstractmethod
  def insert(self, deligence: Deligence):
    """
    指定されたDeligenceを記録する
    """
    raise NotImplementedError
