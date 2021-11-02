import json

from django.test import TestCase, Client

from apps.users.models import User


class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            name="아무개",
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup(self):
        client = Client()
        user = {
            'name': '아무개1',
        }
        response = client.post('/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "user created"})

    def test_fail_signup(self):
        client = Client()
        user = {
            'name': '아무개',
        }
        response = client.post('/signup', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "duplicate"})
