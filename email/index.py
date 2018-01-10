import boto3
import os

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')


def send_email(mail, tag, url):
    source = os.environ['SOURCE']

    print('Sending email to %s for tag %s' % (mail, tag))

    ses_client.send_email(
        Source=source,
        Destination={
            'ToAddresses': [
                mail,
            ]
        },
        Message={
            'Subject': {
                'Data': 'Your tweets with hastag #' + tag,
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': 'Hi,\nClick the url to download your mp3 file:\n\n' + url,
                    'Charset': 'utf-8'
                }
            }
        }
    )


def extract_email_and_tag(key):
    result = str.split(key, 'audio/')[1]
    result = str.split(result, '-hashtag-')
    email = result[0].replace('***', '@')
    tag = str.split(result[1], '.mp3')[0]

    return email, tag


def extract_bucket_and_key_from_event(event):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    return bucket, key


def generate_url(bucket, key):
    return s3_client.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket, 'Key': key},
                                            ExpiresIn=7200)


def my_handler(event, context):
    bucket, key = extract_bucket_and_key_from_event(event)
    url = generate_url(bucket, key)

    email, tag = extract_email_and_tag(key)
    send_email(email, tag, url)

    return {
        'message': 'email dispatched to ' + email
    }
