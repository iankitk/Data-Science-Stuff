
class Config:

    ROOT_DIR = "C:\\Users\\ianki\\Desktop\\Intern\\xbrl"
    ROOT_INPUT_DIR = f"{ROOT_DIR}\\input"
    ROOT_OUTPUT_DIR = f"{ROOT_DIR}\\output"
    ROOT_CIENA_STAGE_DIR = f"{ROOT_DIR}\\ciena_stage"
    ROOT_CIENA_FINAL_DIR = f"{ROOT_DIR}\\ciena"
    XBRL_SOURCE_BUCKET_NAME = "digital-alpha-xbrl-source-files"
    XBRL_STAGING_BUCKET_NAME = "digital-alpha-xbrl-staging-files"

    @staticmethod
    def file_prefix(ticker, year, quarter):
        return  f"{ticker}_{year}_{quarter}".lower()

    @staticmethod
    def get_s3_path(ticker, year, quarter, doc_type, file_name):
        return  f"{year}/q{quarter}/{doc_type}/{ticker}/{file_name}".lower()