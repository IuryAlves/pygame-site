# coding: utf-8

import os
import sys
import unittest
import json

PROJECT_PATH = os.path.sep.join(
    os.path.abspath(__file__).split(os.path.sep)[:-3]
)
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

from app.contents import usecase as content_usecase
import app


class ContentApiTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.db.create_all()

    def setUp(self):
        self.client = app.Flask.test_client(app.app)
        content_usecase.delete_all_contents()

    def test_get_contents(self):

        response = self.client.get("/api/contents/get")
        data = json.loads(response.data)
        contents = data["data"]

        self.assertEqual(len(contents), 0)

        content_usecase.add_content("<p>teste</p>", "downloads")

        response = self.client.get("/api/contents/get")
        data = json.loads(response.data)
        contents = data["data"]

        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0],
                         {"data": "<p>teste</p>",
                          "type_": "downloads"
                          })

    def test_add_content(self):

        data = json.dumps(
            {"data": "<p> oba oba boa ee </p>", "type_": "downloads"})
        response = self.client.post("/api/contents/add", data=data)
        self.assertEqual(response.status_code, 200)

    def test_remove_content(self):
        content_usecase.add_content("<p> oba oba boa ee </p>", "downloads")
        data = json.dumps({"type_": "downloads"})
        response = self.client.post("/api/contents/delete", data=data)

        self.assertEqual(response.status_code, 200)

    def test_edit_content(self):
        content_usecase.add_content("<p> oba oba boa ee </p>", "downloads")

        data = json.dumps({"data": "<p>  ahoi </p>", "type_": "downloads"})
        response = self.client.post("/api/contents/edit", data=data)

        json_data = json.loads(response.data)
        data = json_data["data"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"], "<p>  ahoi </p>")

if __name__ == '__main__':
    unittest.main()
