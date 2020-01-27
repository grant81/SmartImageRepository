import unittest
from unittest.mock import MagicMock
import mock
import io
import os
os.environ['SEARCH_SERVICE_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'test'
os.environ['POSTGRES_USER'] = 'test'
os.environ['POSTGRES_PASSWORD'] = 'test'
os.environ['POSTGRES_HOST'] = 'localhost'
import app


class TestTagService(unittest.TestCase):
    @mock.patch('app.PostgresImageDBController')
    def setUp(self, PostgresImageDBController) -> None:
        self.tagService = app.create_app()
        self.tagService.config['TESTING'] = True
        self.tagService = self.tagService.test_client()

    def test_save(self):
        with open("test_image.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
            data = {'file': (io.BytesIO(b), "file"), 'url': 'test/path'}
            res = self.tagService.post('/save',data = data)
        app.postgres.add_image_with_tags.assert_called_once()
        self.assertEqual(['elephant'], res.get_json()['tags'],'Should produce correct tag')

    def test_search(self):
        mock_response = {'urls':"abc/def"}
        app.send_search_request = MagicMock('send_search_request',return_value = mock_response)

        with open("test_image.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
            data = {'file': (io.BytesIO(b), "file")}
            self.tagService.post('/search', data=data)
        app.send_search_request.assert_called_once()

    def test_detector(self):
        with open("test_image.jpg", "rb") as image:
            f = image.read()
            b = bytearray(f)
            tags = app.detector.produce_tag(b)
            self.assertEqual(['elephant'], tags, 'Should produce correct tag')
