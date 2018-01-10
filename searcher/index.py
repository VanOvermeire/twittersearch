import urllib.parse
import boto3
import os
from application_only_auth import Client

base_search_url = 'https://api.twitter.com/1.1/search/tweets.json?count=%d&q=%s'
COUNT = 5

TWEET_BUCKET_PREFIX = 'tweets/'
AT_REPLACER = '***'

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')

BUCKET = os.environ['BUCKET']
TWITTER_KEY = os.environ['TWITTER_KEY']
TWITTER_SECRET = os.environ['TWITTER_SECRET']
client = Client(TWITTER_KEY, TWITTER_SECRET)


def create_key(tag, email):
    # can't have an @ in an s3 key
    email = email.replace("@", AT_REPLACER)

    if '#' in tag:
        tag = tag.replace('#', '')

    return TWEET_BUCKET_PREFIX + email + '/' + tag


def create_s3_data(tweets):
    payload = '\n'.join(tweets)
    return payload


def store_in_s3(data, bucket, key):
    print('Adding key ' + key + ' to bucket ' + bucket)
    s3_client.put_object(Body=data, Bucket=bucket, Key=key)


def get_tweet_text(tag):
    tweet_list = []

    tag = urllib.parse.quote_plus(tag)
    url = base_search_url % (COUNT, tag)

    print('searching for ' + url)
    tweets = client.request(url)

    for status in tweets['statuses']:
        tweet = 'Tweet:' + status['text']
        tweet_list.append(tweet)

    print('Found ' + str(tweet_list))
    return tweet_list


def my_handler(event, context):
    slots = event['currentIntent']['slots']
    email = slots['mail']
    tag = slots['tag']

    print('Received tag %s and mail %s' % (tag, email))
    tweets = get_tweet_text(tag)

    key = create_key(tag, email)
    data = create_s3_data(tweets)

    store_in_s3(data, BUCKET, key)

    return {
        'message': 'handled event for tag %s and mail %s' % (tag, email)
    }
