from config import DETAIL
from datetime import date


class DeligenceModel:
    def __init__(self, data):
        super().__init__()
        self.doc_id = data['doc_id']
        self.current_year_operating_income = data['current_year_operating_income']
        self.prior_1year_operating_income = data['prior_1year_operating_income']
        self.current_year_current_assets = data['current_year_current_assets']
        self.current_year_investments_and_other_assets = data[
            'current_year_investments_and_other_assets']
        self.current_year_current_liabilities = data['current_year_current_liabilities']
        self.current_year_noncurrent_liabilities = data['current_year_noncurrent_liabilities']
        self.current_year_net_assets = data['current_year_net_assets']
        self.current_year_total_number_of_issued_shares = data[
            'current_year_total_number_of_issued_shares']

    def caluculate_company_value(self):
        # 前期、今期の営業利益をもとに、事業価値を出す
        business_value = (self.current_year_operating_income +
                          self.prior_1year_operating_income) / 2 * 10
        self.print_billion('事業価値', business_value)

        # 流動資産・流動負債、固定資産の一部から財産価値を出す
        property_value = self.current_year_current_assets - \
            (self.current_year_current_liabilities * 1.2) + \
            self.current_year_investments_and_other_assets
        self.print_billion('財産価値', property_value)

        # 借金＝固定負債を引く
        self.print_billion('会社の価値', business_value + property_value -
                           self.current_year_noncurrent_liabilities)
        return business_value + property_value - self.current_year_noncurrent_liabilities

    # 一株あたりの価値を出す
    def value_per_share(self):
        return int(self.caluculate_company_value() * 1000000 / self.current_year_total_number_of_issued_shares)

    # 自己資本比率
    def capital_ratio(self):
        sum = self.current_year_current_liabilities + \
            self.current_year_noncurrent_liabilities + self.current_year_net_assets
        return int(round(100 * (self.current_year_net_assets / sum)))

    def print_billion(self, title: str, value: int):
        if DETAIL:
            print(title, value / 100000000, '(億円)')

    def to_dto(self):
        entity = {
            'doc_id': self.doc_id,
            'value_per_share': self.value_per_share(),
            'capital_ratio': self.capital_ratio(),
            'current_year_operating_income': self.current_year_operating_income,
            'prior_1year_operating_income': self.prior_1year_operating_income,
            'current_year_current_assets': self.current_year_current_assets,
            'current_year_investments_and_other_assets': self.current_year_investments_and_other_assets,
            'current_year_current_liabilities': self.current_year_current_liabilities,
            'current_year_noncurrent_liabilities': self.current_year_noncurrent_liabilities,
            'current_year_net_assets': self.current_year_net_assets,
            'current_year_total_number_of_issued_shares': self.current_year_total_number_of_issued_shares,
            'updated_at': date.today(),
        }
        return entity


def contruct_by_xbrl_dict(doc_id, xbrl_dict):
    data = {
        'doc_id': doc_id,
        'current_year_operating_income': million(xbrl_dict['当期営業利益']),
        'prior_1year_operating_income': million(xbrl_dict['前期営業利益']),
        'current_year_current_assets': million(xbrl_dict['当期流動資産合計']),
        'current_year_investments_and_other_assets': million(
            xbrl_dict['当期その他の資産合計']),
        'current_year_current_liabilities': million(xbrl_dict['当期流動負債合計']),
        'current_year_noncurrent_liabilities': million(xbrl_dict['当期固定負債合計']),
        'current_year_net_assets': million(xbrl_dict['当期純資産合計']),
        'current_year_total_number_of_issued_shares': int(float((
            xbrl_dict['当期発行済株式総数']))),
    }
    return DeligenceModel(data)


def million(value_str: str):
    value = int(value_str)
    return round(value / 1000000, 0)
