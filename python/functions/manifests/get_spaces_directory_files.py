import os
from dotenv import load_dotenv
import boto3


# boto3.set_stream_logger('botocore', level='DEBUG')

load_dotenv()

config = {
    'region_name': 'sfo2',
    'endpoint_url': 'https://sfo2.digitaloceanspaces.com/',
    'aws_access_key_id': os.environ.get("aws_key"),
    'aws_secret_access_key': os.environ.get("aws_secret")
}

bucket_endpoint = 'https://acip.sfo2.digitaloceanspaces.com/'


def get_spaces_directory_files(spaces_dir):

    session = boto3.session.Session()
    # client is low level, returns dicts
    # client = session.client('s3', **config)

    # resource is high level and generally returns instances of bucket / objects
    # if you need client you can access through resource.meta.client (as below)
    resource = session.resource('s3', **config)

    # response = client.list_objects(Bucket='acip')
    paginator = resource.meta.client.get_paginator('list_objects')
    operation_parameters = {
        'Bucket': 'acip',
        'Prefix': f'scans/published/{spaces_dir}/',
        'Delimiter': '/'
    }

    page_iterator = paginator.paginate(**operation_parameters)

    image_listing = {}
    # paginate
    for page in page_iterator:
        # page contents correspond to image groups
        images = []
        page_key = page['ResponseMetadata'].get('RequestId', 'some_key')  # need a random key gen if no req id present
        for group in page['Contents']:
            [dir_path, image_name] = os.path.split(group.get('Key'))
            images.append(os.path.join(bucket_endpoint, dir_path, image_name))

        image_listing.update({page_key: images})

    return image_listing
