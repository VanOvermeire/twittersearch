import boto3
from twittersearchhelpers import twitter_polly, twitter_s3

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')
polly_client = boto3.client('polly')


def my_handler(event, context):
    bucket, key = twitter_s3.extract_bucket_and_key_from_event(event)
    text = twitter_s3.get_s3_object_as_string(s3_client, bucket, key)
    filename = twitter_s3.generate_audio_filename(key)

    print('Writing to bucket ' + bucket + ' with filename ' + filename)
    twitter_polly.write_audio_to_file(polly_client, bucket, filename, text)

    return {
        'message': 'create audio for ' + key
    }
