import unittest
from mail import index


class TestHelpers(unittest.TestCase):

    def test_extract_email_and_tag(self):
        key = 'audio/test***test.com-hashtag-example'

        email, tag = index.extract_email_and_tag(key)

        self.assertTrue(email, 'test@test.com')
        self.assertTrue(tag, 'example')


if __name__ == '__main__':
    unittest.main()
