
import boto3  # REQUIRED! - Details here: https://pypi.org/project/boto3/
from botocore.exceptions import ClientError
from botocore.config import Config

def get_b2_resource(endpoint, key_id, application_key):
    b2 = boto3.resource(service_name='s3',
                        endpoint_url=endpoint,                # Backblaze endpoint
                        aws_access_key_id=key_id,              # Backblaze keyID
                        aws_secret_access_key=application_key, # Backblaze applicationKey
                        config = Config(
                            signature_version='s3v4',
                    ))
    return b2

def upload_file(bucket, directory, file, b2, b2path=None):
    file_path = directory + '/' + file
    remote_path = b2path
    if remote_path is None:
        remote_path = file
    try:
        response = b2.Bucket(bucket).upload_file(file_path, remote_path)
    except ClientError as ce:
        print('error', ce)

    return response

def list_object_keys(bucket, b2):
    try:
        response = b2.Bucket(bucket).objects.all()

        return_list = []               # create empty list
        for object in response:        # iterate over response
            return_list.append(object.key) # for each item in response append object.key to list
        return return_list             # return list of keys from response

    except ClientError as ce:
        print('error', ce)

b2 = get_b2_resource(endpoint, key_id, application_key)

b2.Bucket(bucket).upload_file("google_logo.jpg", "abc/logo2.jpg")

print(list_object_keys(bucket, b2))

