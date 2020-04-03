from config import TARGET_COMPANY_LIST

TARGET_FORM_CODE_LIST = [
    '030000',  # 有価証券報告書
    # '043000',  # 四半期報告書
]


class Company:
    def __init__(self, data):
        super().__init__()
        self.filer_name = data['filerName']
        self.doc_id = data['docID']
        self.form_code = data['formCode']
        if type(data['secCode']) is str:
            self.sec_code = data['secCode'][0:len(data['secCode']) - 1]
        else:
            self.sec_code = ''

    def is_target_financial_report(self):
        return self.form_code in TARGET_FORM_CODE_LIST and self.sec_code in TARGET_COMPANY_LIST

    def generate_doc_url(self):
        # ex.) https://disclosure.edinet-fsa.go.jp/api/v1/documents/S100IA9D?type=1
        return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/' + self.doc_id + '?type=1'
