import boto3

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')
polly_client = boto3.client('polly')

AUDIO_BUCKET_PREFIX = 'audio/'
CHUNK_SIZE = 1024
TMP_FILE = '/tmp/temp.mp3'


def write_audio_to_file(bucket, filename, text):
    # for now just taking an english voice
    response = polly_client.synthesize_speech(OutputFormat='mp3', VoiceId='Joanna', Text=text)
    stream = response.get('AudioStream')

    with open(TMP_FILE, 'wb') as filewriter:
        while True:
            data = stream.read(CHUNK_SIZE)
            filewriter.write(b"%X\r\n%s\r\n" % (len(data), data))

            if not data:
                break
        # Ensure any buffered output has been transmitted and close the stream
        filewriter.flush()

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(TMP_FILE, bucket, AUDIO_BUCKET_PREFIX + filename)


def get_s3_object_as_string(bucket, key):
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    s3_object = s3_object['Body'].read()
    return s3_object.decode('utf-8')


def extract_bucket_and_key_from_event(event):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    return bucket, key


def generate_filename(key):
    filename = key.replace('tweets/', '')

    tag = str.split(key, '***')[1]
    tag = str.split(tag, '/')[1]

    filename = str.split(filename, '/' + tag)[0] + '-hashtag-' + tag
    filename = filename + '.mp3'

    return filename


def my_handler(event, context):
    bucket, key = extract_bucket_and_key_from_event(event)

    text = get_s3_object_as_string(bucket, key)
    filename = generate_filename(key)

    print('Writing to bucket ' + bucket + ' with filename ' + filename)
    write_audio_to_file(bucket, filename, text)

    return {
        'message': 'create audio for ' + key
    }
