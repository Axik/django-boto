import unittest
import random
import string

from django_boto.s3.storage import S3Storage
from django.core.files.storage import default_storage
from .utils import AWSMockServiceTestCase


"""
https://github.com/boto/boto/blob/develop/tests/unit/s3/test_bucket.py

Definitely guide of how write tests to s3 storage.

"""


def get_string(lngth):
    strn = ''

    for i in range(lngth):
        strn += random.choice(string.ascii_letters)

    return strn


class TestStorageBasic(unittest.TestCase):

    def test_repr(self):
        self.assertEqual(repr(S3Storage(bucket_name='test')),
                         'S3 Bucket Storage test')

    def test_get_auth_from_settings(self):
        self.assertIsInstance(default_storage, S3Storage)
        self.assertEqual(default_storage.bucket_name, 'test_name')
        self.assertEqual(default_storage.key, 'test_key')
        self.assertEqual(default_storage.secret, 'test_secret')
        self.assertEqual(default_storage.location, 'ap-southeast-2')


class TestStorageS3(AWSMockServiceTestCase):

    def setUp(self):
        super(TestStorageS3, self).setUp()
        self.storage = S3Storage(bucket_name='test')
        self.storage.get_connection = lambda: self.service_connection

    def test_exists(self):
        self.set_http_response(status_code=200)
        self.assertTrue(self.storage.exists('some_name'))

    def test_bucket_create_bucket(self):
        self.set_http_response(status_code=200)
        bucket = self.service_connection.create_bucket('mybucket_create')
        self.assertEqual(bucket.name, 'mybucket_create')
