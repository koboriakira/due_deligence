from abc import ABCMeta, abstractmethod
from due_deligence.interactor.analyze_requestor import AnalyzeRequestor
from due_deligence.interactor import analyzer

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


class AnalyzeGenerator(AnalyzeRequestor):

  def analyze_company(self, company):
    deligence = analyzer.get_deligence(company)
    if deligence is None:
        return

    print('1株あたりの価値', deligence.value_per_share(), '(円)')

    # stock_price = scrape_stock_price.scrape_stock_price(company)
    # if not stock_price is None:
    #     print('株価', stock_price, '(円)')
    #     print('安全圏', _underpriced(stock_price,
    #                              deligence.value_per_share()), '(%)')

  def analyze_company_list(self, company_list):
    for company in company_list:
        print('*****', company.to_str(), '*****')
        self.analyze(company)
        print('============================\n\n')

  def _underpriced(self, stock_price, value_per_share):
    """
    安全圏、割安度を確認
    """
    return round(100 * stock_price / value_per_share, 0)
