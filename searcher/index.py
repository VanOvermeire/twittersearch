import urllib.parse
import boto3
import os
from application_only_auth import Client

base_search_url = 'https://api.twitter.com/1.1/search/tweets.json?count=%d&q=%s'
COUNT = 5

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')

BUCKET = os.environ['BUCKET']
TWITTER_KEY = os.environ['TWITTER_KEY']
TWITTER_SECRET = os.environ['TWITTER_SECRET']
client = Client(TWITTER_KEY, TWITTER_SECRET)


def create_key(tag, email):
    email = email.split('@')[0]

    if '#' in tag:
        tag = tag.replace('#', '')

    return email + '/' + tag


def store_in_s3(tweets, bucket, key):
    payload = '\n'.join(tweets)
    print('Adding key ' + key + ' to bucket ' + bucket)
    s3_client.put_object(Body=payload, Bucket=bucket, Key=key)


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

    print('Received tag %s and email %s' % (tag, email))
    tweets = get_tweet_text(tag)

    key = create_key(tag, email)
    store_in_s3(tweets, BUCKET, key)

    return {
        'message': 'handled event for tag %s and email %s' % (tag, email)
    }
