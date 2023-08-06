import unittest
from sdklib.util.files import guess_filename_stream

from tests.sample_sdk import SampleHttpSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SampleHttpSdk.set_default_proxy("http://localhost:8080")
        cls.api = SampleHttpSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def _test_get_items(self):
        response = self.api.get_items()
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.data, list))

    def _test_create_item(self):
        response = self.api.create_item("mi nombre", "algo")
        self.assertEqual(response.status, 201)

    def _test_update_item(self):
        response = self.api.update_item(1, "mi nombre", "algo")
        self.assertEqual(response.status, 200)

    def _test_partial_update_item(self):
        response = self.api.partial_update_item(1, "mi nombre")
        self.assertEqual(response.status, 405)

    def _test_delete_item(self):
        response = self.api.delete_item(1)
        self.assertEqual(response.status, 204)

    def _test_login(self):
        response = self.api.login(username="user", password="password")
        self.assertEqual(response.status, 404)

    def _test_create_file(self):
        fname, fstream = guess_filename_stream("tests/resources/file.pdf")
        response = self.api.create_file_11paths_auth(fname, fstream, "235hWLEETQ46KWLnAg48",
                                                     "lBc4BSeqtGkidJZXictc3yiHbKBS87hjE078rswJ")
        self.assertEqual(response.status, 404)
