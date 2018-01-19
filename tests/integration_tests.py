from twittersearchhelpers import twitter_s3
from moto import mock_s3
import boto3
import os

EXAMPLE_BUCKET = 'examplebucket'
EXAMPLE_KEY = 'our_key'


@mock_s3
def test_get_signed_url():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=EXAMPLE_BUCKET)
    s3_client.put_object(Bucket=EXAMPLE_BUCKET, Key=EXAMPLE_KEY, Body=b'this is some data')

    url = twitter_s3.generate_url(s3_client, EXAMPLE_BUCKET, EXAMPLE_KEY)

    assert len(url) > 0
    assert 'examplebucket' in url
    assert 'our_key' in url


@mock_s3
def test_put_s3_object():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=EXAMPLE_BUCKET)
    os.environ['BUCKET'] = EXAMPLE_BUCKET # fake the environment variable

    twitter_s3.store_in_s3(s3_client, 'here is some data', EXAMPLE_KEY)

    response = s3_client.list_objects_v2(Bucket=EXAMPLE_BUCKET)

    assert len(response['Contents']) == 1


@mock_s3
def test_get_s3_object():
    s3_client = boto3.client('s3')
    s3_client.create_bucket(Bucket=EXAMPLE_BUCKET)
    s3_client.put_object(Bucket=EXAMPLE_BUCKET, Key=EXAMPLE_KEY, Body=b'this is some data')

    response_string = twitter_s3.get_s3_object_as_string(s3_client, EXAMPLE_BUCKET, EXAMPLE_KEY)

    assert 'this is some data' in response_string
