import json
import unittest
from abc import ABCMeta, abstractmethod
from werkzeug.datastructures import Headers
from nose_tests.setup_tests import SetupTests


class NDTestCase(unittest.TestCase, metaclass=ABCMeta):
    @classmethod
    def setUpClass(cls):
        cls._setup = SetupTests()

    @classmethod
    def tearDownClass(cls):
        cls._setup.master_test_teardown()

    @abstractmethod
    def setUp(self):
        self.app = self._setup.app

    def dict_from_response(self, response):
        return json.loads(response.data.decode('unicode_escape'))

    def build_headers(self, data_json=False):
        headers = Headers()

        if data_json:
            headers.add('Content-Type', 'application/json')

        return headers

    def json_get(self, uri):
        return self.app.get(uri, headers=self.build_headers())

    def json_post(self, uri, post_data, data_json=False):
        if data_json:
            post_data = json.dumps(post_data)

        return self.app.post(uri, data=post_data,
                             headers=self.build_headers(data_json=data_json))

    def json_delete(self, uri):
        return self.app.delete(uri, headers=self.build_headers())
