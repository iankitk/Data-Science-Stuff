class ExecutionProps:
    year: int
    ticker: str
    quarter: int
    doc_type: str
    xbrl_instance_path: str
    xbrl_label_path: str
    xbrl_presentation_path: str
    xbrl_calc_path: str
    xbrl_schema_path: str

    def __init__(self, *, ticker, year, quarter, doc_type, xbrl_instance_path, xbrl_label_path,
        xbrl_presentation_path, xbrl_calc_path, xbrl_schema_path):
        self.year = year
        self.ticker = ticker
        self.quarter = quarter
        self.doc_type = doc_type
        self.xbrl_instance_path = xbrl_instance_path
        self.xbrl_label_path = xbrl_label_path
        self.xbrl_calc_path = xbrl_calc_path
        self.xbrl_presentation_path = xbrl_presentation_path
        self.xbrl_schema_path = xbrl_schema_path