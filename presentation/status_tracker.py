import boto3
import requests
import traceback
import botocore

class StatusTracker:

    def __init__(self):
        self.client = boto3.resource("dynamodb")
        pass

    def update_row(self, *, ticker, year, quarter, document_type, data):
        row = self.get_row(ticker=ticker, year=year, quarter=quarter, document_type=document_type)

        if row is not None:
            row_key = f'{ticker}_{year}_{quarter}_{document_type}'.lower()
            merged_row = {**row, **data}
            table = self.client.Table("ticker-quarterly-statuses")

            try:
                response = table.put_item(Item=merged_row)
            except botocore.exceptions.ClientError as e:
                print(e.response['Error']['Message'])
                traceback.print_exc()
            else:
                return response['Item'] if 'Item' in response else None
            
        return None


    def get_row(self, *, ticker, year, quarter, document_type):
        row_key = f'{ticker}_{year}_{quarter}_{document_type}'.lower()
        table = self.client.Table("ticker-quarterly-statuses")

        try:
            response = table.get_item(Key={'ticker_key': row_key})
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Message'])
            traceback.print_exc()
        else:
            return response['Item'] if 'Item' in response else None
        
        return None
        