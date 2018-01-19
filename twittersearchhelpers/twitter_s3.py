TWEET_BUCKET_PREFIX = 'tweets/'
AT_REPLACER = '***'


def extract_bucket_and_key_from_event(event):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    return bucket, key


def create_s3_data(tweets):
    payload = '\n'.join(tweets)
    return payload


def create_tweet_key(tag, email):
    # can't have an @ in an s3 key
    email = email.replace("@", AT_REPLACER)

    if '#' in tag:
        tag = tag.replace('#', '')

    return TWEET_BUCKET_PREFIX + email + '/' + tag


def generate_audio_filename(key):
    filename = key.replace('tweets/', '')

    tag = str.split(key, '***')[1]
    tag = str.split(tag, '/')[1]

    filename = str.split(filename, '/' + tag)[0] + '-hashtag-' + tag
    filename = filename + '.mp3'

    return filename


def get_s3_object_as_string(client, bucket, key):
    s3_object = client.get_object(Bucket=bucket, Key=key)
    s3_object = s3_object['Body'].read()
    return s3_object.decode('utf-8')


def store_in_s3(client, data, bucket, key):
    print('Adding key ' + key + ' to bucket ' + bucket)
    client.put_object(Body=data, Bucket=bucket, Key=key)


def generate_url(client, bucket, key):
    return client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=7200)
