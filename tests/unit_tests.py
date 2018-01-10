import unittest
from mail import index as mail_index
from speech import index as speech_index


class TestHelpers(unittest.TestCase):

    def test_extract_email_and_tag(self):
        key = 'audio/test***test.com-hashtag-example'

        email, tag = mail_index.extract_email_and_tag(key)

        self.assertTrue(email, 'test@test.com')
        self.assertTrue(tag, 'example')

    def test_extract_bucket_and_key(self):
        s3 = dict()
        s3['bucket'] = {'name': 'example-bucket'}
        s3['object'] = {'key': 'audio/test***test.com-hashtag-example'}

        event = dict()
        event['Records'] = [{'s3': s3}]

        bucket, key = mail_index.extract_bucket_and_key_from_event(event)

        self.assertTrue(bucket, 'example-bucket')
        self.assertTrue(key, 'audio/test***test.com-hashtag-example')

    def test_generate_filename(self):
        key = 'tweets/test***test.com/example'

        filename = speech_index.generate_filename(key)

        self.assertTrue('test***test.com-hashtag-example.mp3', filename)


if __name__ == '__main__':
    unittest.main()
