import urllib.parse
import boto3
import os
from application_only_auth import Client
from twittersearchhelpers import twitter_s3

base_search_url = 'https://api.twitter.com/1.1/search/tweets.json?count=%d&q=%s'
COUNT = 5

# doing this outside the lambda is better for performance
s3_client = boto3.client('s3')

TWITTER_KEY = os.environ['TWITTER_KEY']
TWITTER_SECRET = os.environ['TWITTER_SECRET']
client = Client(TWITTER_KEY, TWITTER_SECRET)


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

    key = twitter_s3.create_tweet_key(tag, email)
    data = twitter_s3.create_s3_data(tweets)

    twitter_s3.store_in_s3(s3_client, data, key)

    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Done. Your tweets will be arriving in your inbox shortly!"
            }
        }
    }
