import unittest
from tests import BaseAPITestCase


class CompressTestCase(BaseAPITestCase):
    def test_mimetypes(self):
        defaults = [
            "text/html",
            "text/css",
            "application/json",
            "application/javascript",
        ]
        self.assertEqual(self.app.config["COMPRESS_MIMETYPES"], defaults)

    def test_level(self):
        self.assertEqual(self.app.config["COMPRESS_LEVEL"], 6)

    def test_min_size(self):
        self.assertEqual(self.app.config["COMPRESS_MIN_SIZE"], 500)

    def test_status_code(self):
        headers = [("Accept-Encoding", "gzip")]
        response = self.client.options("/", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_content_encoding(self):
        headers = [("Accept-Encoding", "gzip")]
        response = self.client.options("/", headers=headers)
        self.assertEqual(response.content_encoding, "gzip")


if __name__ == '__main__':
    unittest.main()
