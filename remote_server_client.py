
import boto3  # REQUIRED! - Details here: https://pypi.org/project/boto3/
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime, timedelta


class RemoteServerClient():
    def __init__(self, config):
        self.cfg = config
        self.b2 = boto3.resource(service_name='s3',
                        endpoint_url=self.cfg.get('endpoint'),
                        aws_access_key_id=self.cfg.get('key_id'),
                        aws_secret_access_key=self.cfg.get('application_key'), 
                        config = Config(
                            signature_version='s3v4',
                    ))
        self.delete_old_files(self.cfg.get('delete_images_after_n_days'))

    def delete_old_files(self, days_threshold):
         threshold_date = datetime.now() - timedelta(days=days_threshold)
         for obj in self.b2.Bucket(self.cfg.get('bucket')).objects.all():
            last_modified = obj.last_modified
            if last_modified < threshold_date:
                object_key = obj.key
                print(f'Deleting object: {object_key}')
                obj.delete()

    def download_file(self, key_name, local_fname):
        try:
            self.b2.Bucket(self.cfg.get('bucket')).download_file(key_name, local_fname)
        except ClientError as ce:
            print('error', ce)

    def get_file(self, key_name):
        try:
            response = self.b2.get_object(Bucket=self.cfg.get('bucket'), Key=key_name)
            return response['Body'].read()
        except ClientError as ce:
            print('error', ce)

    def get_file_info_list(self):
        try:
            response = self.b2.Bucket(self.cfg.get('bucket')).objects.all()
            file_list = []
            for obj in response:
                info = (obj.key, obj.last_modified.timestamp())
                file_list.append(info)
            return file_list
        except ClientError as ce:
            print('error', ce)

    def upload_file(self, fname, b2fname=None):
        if b2fname is None:
            b2fname = fname
        try:
            self.b2.Bucket(self.cfg.get('bucket')).upload_file(fname, b2fname)
        except ClientError as ce:
            print('error', ce) 