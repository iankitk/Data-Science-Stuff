import boto3
import requests
import botocore
from config import Config
import traceback

class FileAccess:

    def __init__(self):
        self.s3 = boto3.resource('s3')
        pass

    def file_exists(self, *, bucket_name, file_path):
        try:
            s3_client = boto3.client('s3', 'us-east-1')
            print(bucket_name)
            print(file_path)
            s3_client.head_object(Bucket=bucket_name, Key=file_path)

        except botocore.exceptions.ClientError as e:
            traceback.print_exc()
            print(e.response['Error'])
            if e.response['Error']['Code'] == "404":
                return False
        else:
            return True

    def get_file(self, *, bucket_name, file_path):
        if self.file_exists(bucket_name=bucket_name, file_path=file_path):
            obj = self.s3.Object(bucket_name=bucket_name, key=file_path).get()
            return obj['Body'].read().decode('utf-8')
        else:
            return None

    def put_file(self, *, bucket_name, ticker, year, quarter, doc_type, file_name, content):
        path = Config.get_s3_path(ticker, year, quarter, doc_type, file_name)
        obj = self.s3.Object(bucket_name=bucket_name, key=path)
        obj.put(Body=content)
        return path
        