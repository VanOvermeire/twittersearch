import boto3
from twittersearchhelpers import twitter_ses, twitter_s3

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')


def my_handler(event, context):
    bucket, key = twitter_s3.extract_bucket_and_key_from_event(event)
    url = twitter_s3.generate_url(s3_client, bucket, key)

    email, tag = twitter_s3.extract_email_and_tag_from_audio_key(key)
    twitter_ses.send_email(ses_client, email, tag, url)

    return {
        'message': 'mail dispatched to ' + email
    }
