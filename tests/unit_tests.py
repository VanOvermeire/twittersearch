import unittest
from twittersearchhelpers import twitter_s3


class TestHelpers(unittest.TestCase):

    def test_extract_email_and_tag(self):
        key = 'audio/test***test.com-hashtag-example'

        email, tag = twitter_s3.extract_email_and_tag_from_audio_key(key)

        self.assertTrue(email, 'test@test.com')
        self.assertTrue(tag, 'example')

    def test_extract_bucket_and_key(self):
        s3 = dict()
        s3['bucket'] = {'name': 'example-bucket'}
        s3['object'] = {'key': 'audio/test***test.com-hashtag-example'}

        event = dict()
        event['Records'] = [{'s3': s3}]

        bucket, key = twitter_s3.extract_bucket_and_key_from_event(event)

        self.assertTrue(bucket, 'example-bucket')
        self.assertTrue(key, 'audio/test***test.com-hashtag-example')

    def test_generate_filename(self):
        key = 'tweets/test***test.com/example'

        filename = twitter_s3.generate_audio_filename(key)

        self.assertTrue('test***test.com-hashtag-example.mp3', filename)

    def test_create_s3_data(self):
        tweets = ['first tweet', 'second tweet', 'third tweet']

        result = twitter_s3.create_s3_data(tweets)

        self.assertEqual(len(result), 36)
        self.assertTrue('first tweet' in result)

    def test_create_empty_s3_data(self):
        tweets = []

        result = twitter_s3.create_s3_data(tweets)

        self.assertEqual(len(result), 0)

    def test_create_tweet_key_with_hashtag_included(self):
        tag = '#aws'
        email = 'test@test.com'

        result = twitter_s3.create_tweet_key(tag, email)

        self.assertEqual(result, 'tweets/test***test.com/aws')

    def test_create_tweet_key_no_hashtag(self):
        tag = 'aws'
        email = 'test@test.com'

        result = twitter_s3.create_tweet_key(tag, email)

        self.assertEqual(result, 'tweets/test***test.com/aws')

    def test_create_audio_filename(self):
        key = 'tweets/test***test.com/aws'

        result = twitter_s3.generate_audio_filename(key)

        self.assertEqual(result, 'test***test.com-hashtag-aws.mp3')


if __name__ == '__main__':
    unittest.main()
