from config import DETAIL


class DeligenceModel:
    def __init__(self, xbrl_dict):
        super().__init__()
        self.current_year_operationg_income = int(xbrl_dict['当期営業利益'])
        self.prior_1year_operationg_income = int(xbrl_dict['前期営業利益'])
        self.current_year_current_assets = int(xbrl_dict['当期流動資産合計'])
        self.current_year_investments_and_other_assets = int(
            xbrl_dict['当期その他の資産合計'])
        self.current_year_current_liabilities = int(xbrl_dict['当期流動負債合計'])
        self.current_year_noncurrent_liabilities = int(xbrl_dict['当期固定負債合計'])
        self.current_year_net_assets = int(xbrl_dict['当期純資産合計'])
        self.current_year_total_number_of_issued_shares = int(
            xbrl_dict['当期発行済株式総数'])

    def caluculate_company_value(self):
        # 前期、今期の営業利益をもとに、事業価値を出す
        business_value = (self.current_year_operationg_income +
                          self.prior_1year_operationg_income) / 2 * 10
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
        return int(self.caluculate_company_value() / self.current_year_total_number_of_issued_shares)

    # 自己資本比率
    def capital_ratio(self):
        sum = self.current_year_current_liabilities + \
            self.current_year_noncurrent_liabilities + self.current_year_net_assets
        return int(round(100 * (self.current_year_net_assets / sum)))

    def print_billion(self, title: str, value: int):
        if DETAIL:
            print(title, value / 100000000, '(億円)')
