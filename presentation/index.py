from status_tracker import StatusTracker
from file_access import FileAccess
from xbrl_ui_generator import XbrlUiGenerator
from execution_props import ExecutionProps
from config import Config

class Executor:

    def __init__(self):
        pass

    def execute(self, props: ExecutionProps):
        file_access = FileAccess()
        instance_file = file_access.get_file(bucket_name=Config.XBRL_SOURCE_BUCKET_NAME, file_path=props.xbrl_instance_path)
        label_file = file_access.get_file(bucket_name=Config.XBRL_SOURCE_BUCKET_NAME, file_path=props.xbrl_label_path)
        presentation_file = file_access.get_file(bucket_name=Config.XBRL_SOURCE_BUCKET_NAME, file_path=props.xbrl_presentation_path)
        calc_file = file_access.get_file(bucket_name=Config.XBRL_SOURCE_BUCKET_NAME, file_path=props.xbrl_calc_path)
        schema_file = file_access.get_file(bucket_name=Config.XBRL_SOURCE_BUCKET_NAME, file_path=props.xbrl_schema_path)

        xbrl_gen = XbrlUiGenerator()
        xbrl_gen.generate(ticker=props.ticker, year=props.year, quarter=props.quarter, doc_type=props.doc_type,
            data_val=instance_file, data_lab=label_file, data_pre=presentation_file, data_calc=calc_file, data_schema=schema_file)


def handler(event, context):

    payload = event['payload']
    ticker = payload['ticker']
    year = payload['year']
    quarter = payload['quarter']
    doc_type = payload['doc_type']

    dynamo_row = StatusTracker().get_row(ticker=ticker, year=year, quarter=quarter, document_type=doc_type)
    if dynamo_row is not None:
        xbrl_instance_path = dynamo_row['xbrl_instance_path']
        xbrl_label_path = dynamo_row['xbrl_label_path']
        xbrl_presentation_path = dynamo_row['xbrl_presentation_path']
        xbrl_calc_path = dynamo_row['xbrl_calc_path']
        xbrl_schema_path = dynamo_row['xbrl_schema_path']
        executor = Executor()
        props = ExecutionProps(ticker=ticker, year=year, quarter=quarter, doc_type=doc_type, xbrl_instance_path=xbrl_instance_path,
            xbrl_label_path=xbrl_label_path, xbrl_presentation_path=xbrl_presentation_path, xbrl_calc_path=xbrl_calc_path, xbrl_schema_path=xbrl_schema_path)

        executor.execute(props)
    else:
        print("dynamo db row not found..exiting function.")

if __name__ == "__main__":
    event = {
        "payload": {
            "ticker": "LITE",
            "year": 2020,
            "quarter": 3,
            "doc_type": "10-Q"
        }
    }
    handler(event, {})