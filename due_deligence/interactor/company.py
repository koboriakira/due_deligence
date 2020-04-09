from due_deligence.config import TARGET_COMPANY_LIST

TARGET_FORM_CODE_LIST = [
    '030000',  # 有価証券報告書
    # '043000',  # 四半期報告書
]

# 同じ030000でも350「大量保有報告書」の場合もあるので絞り込む
TARGET_DOC_TYPE_CODE = '120'


class Company:
    def __init__(self, doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name):
        self.doc_id = doc_id
        self.date = date
        self.seq_number = seq_number
        self.edinet_code = edinet_code
        self.sec_code = sec_code
        self.form_code = form_code
        self.doc_type_code = doc_type_code
        self.filer_name = filer_name

    def is_financial_report(self):
        return self.form_code in TARGET_FORM_CODE_LIST and self.doc_type_code == TARGET_DOC_TYPE_CODE and self.sec_code is not None

    def generate_doc_url(self):
        # ex.) https://disclosure.edinet-fsa.go.jp/api/v1/documents/S100IA9D?type=1
        return 'https://disclosure.edinet-fsa.go.jp/api/v1/documents/' + self.doc_id + '?type=1'

    def to_entity(self):
        return {
            'doc_id': self.doc_id,
            'date': self.date,
            'seq_number': self.seq_number,
            'edinet_code': self.edinet_code,
            'sec_code': self.sec_code,
            'form_code': self.form_code,
            'doc_type_code': self.doc_type_code,
            'filer_name': self.filer_name,
        }

    @classmethod
    def construct_from_edinet(cls, result, date):
        doc_id = result['docID']
        seq_number = result['seqNumber']
        edinet_code = result['edinetCode']
        sec_code = None
        if type(result['secCode']) is str:
            sec_code = result['secCode'][0:len(result['secCode']) - 1]
        form_code = result['formCode']
        doc_type_code = result['docTypeCode']
        filer_name = result['filerName']
        return Company(doc_id, date, seq_number, edinet_code, sec_code, form_code, doc_type_code, filer_name)

    def to_str(self):
        return '[' + str(self.date) + '] ' + str(self.sec_code) + ' ' + self.filer_name
