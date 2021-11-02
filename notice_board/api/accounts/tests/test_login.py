import json

from django.test import TestCase, Client

from apps.users.models import User


class LoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            name="아무개",
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_login(self):
        client = Client()
        data = {
            'name': '아무개',
        }
        response = client.post('/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fail_login(self):
        client = Client()
        user = {
            'name': '아무개1',
        }
        response = client.post('/login', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
