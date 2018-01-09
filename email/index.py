
def send_email():
    print('do this...')
    # get client
    # generate download signed key
    # send mail with link


def extract_email_and_tag(key):
    result = str.split(key, '-tag-')
    email = result[0].replace('***', '@')
    tag = result[1]
    return email, tag


def extract_bucket_and_key_from_event(event):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    return bucket, key


def my_handler(event, context):
    bucket, key = extract_bucket_and_key_from_event(event)
    email, tag = extract_email_and_tag(key)

    return {
        'message': 'send email to ' + email
    }
