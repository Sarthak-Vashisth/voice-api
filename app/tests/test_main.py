import unittest
from unittest.mock import patch, MagicMock
from flask import json
from app.main import app


class TestMain(unittest.TestCase):
    @patch("app.main.collection")
    def test_store_success(self, mock_collection):
        # Mock MongoDB update_one method
        mock_collection.update_one.return_value = MagicMock()

        # Create test client
        client = app.test_client()

        # Test payload
        payload = {
            "user_id": "test_user",
            "sentence": "Hello world",
            "words": ["Hello", "world"]
        }

        # Send POST request to /store
        response = client.post("/store", data=json.dumps(payload), content_type="application/json")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json)
        self.assertEqual(response.json["status"], "Saved")
        self.assertIn("data", response.json)
        self.assertEqual(response.json["data"]["sentence"], "Hello world")

    @patch("app.main.collection")
    def test_store_missing_fields(self, mock_collection):
        # Mock MongoDB update_one method
        mock_collection.update_one.return_value = MagicMock()

        # Create test client
        client = app.test_client()

        # Test payload with missing fields
        payload = {
            "user_id": "test_user",
            "words": ["Hello", "world"]
        }

        # Send POST request to /store
        response = client.post("/store", data=json.dumps(payload), content_type="application/json")

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)

    @patch("app.main.collection")
    def test_store_invalid_payload(self, mock_collection):
        # Mock MongoDB update_one method
        mock_collection.update_one.return_value = MagicMock()

        # Create test client
        client = app.test_client()

        # Invalid payload (not JSON)
        payload = "invalid_payload"

        # Send POST request to /store
        response = client.post("/store", data=payload, content_type="application/json")

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)

if __name__ == "__main__":
    unittest.main()
