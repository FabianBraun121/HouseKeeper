
import boto3  # REQUIRED! - Details here: https://pypi.org/project/boto3/
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime, timedelta, timezone
import boto3.session


class RemoteServerClient():
    def __init__(self, config):
        self.cfg = config
        self.delete_old_files(self.cfg.get('delete_images_after_n_days'))

    def create_bucket(self):
        return self.create_resource().Bucket(self.cfg.get('bucket'))

    def delete_all_files(self):
        bucket = self.create_bucket()
        for obj in bucket.objects.all():
            obj.delete()
        
    def delete_old_files(self, days_threshold):
        bucket = self.create_bucket()
        threshold_date = datetime.now().replace(tzinfo=timezone.utc) - \
            timedelta(days=days_threshold)
        for obj in bucket.objects.all():
            last_modified = obj.last_modified.replace(tzinfo=timezone.utc)
            if last_modified < threshold_date:
                object_key = obj.key
                print(f'Deleting object: {object_key}')
                obj.delete()

    def download_file(self, key_name, local_fname):
        try:
            bucket = self.create_bucket()
            bucket.download_file(key_name, local_fname)
        except ClientError as ce:
            print('error', ce)

    def get_file(self, key_name):
        try:
            response = self.create_resource().get_object(
                Bucket=self.cfg.get('bucket'), Key=key_name)
            return response['Body'].read()
        except ClientError as ce:
            print('error', ce)

    def get_file_info_list(self):
        try:
            response = self.create_bucket().objects.all()
            file_list = []
            for obj in response:
                info = (obj.key, obj.last_modified.timestamp())
                file_list.append(info)
            return file_list
        except ClientError as ce:
            print('error', ce)

    def create_resource(self):
        return boto3.resource(
            service_name='s3',
            endpoint_url=self.cfg.get('endpoint'),
            aws_access_key_id=self.cfg.get('key_id'),
            aws_secret_access_key=self.cfg.get('application_key'),
            config=Config(signature_version='s3v4')
        )

    def upload_file(self, fname, b2fname=None):
        if b2fname is None:
            b2fname = fname
        try:
            bucket = self.create_bucket()
            with open(fname, 'rb') as file_content:
                bucket.put_object(Key=b2fname, Body=file_content)
        except Exception as e:
            print('Error uploading file:', e)
