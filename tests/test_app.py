
import unittest
from unittest.mock import patch

from app import app


class AttendanceAppTests(unittest.TestCase):

    def test_home_requires_login(self):
        response = self.client.get("/", follow_redirects=False)
        self.assertIn(response.status_code, (302, 401))

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_login_page_loads(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects(self):
        response = self.client.post("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
