import json

from django.test import TestCase, Client

from apps.users.models import User
from apps.posts.models import Post
import jwt
from notice_board.settings import SECRET_KEY, ALGO


class PostTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            name="아무개",
        )
        Post.objects.create(
            title="제목",
            body="내용",
            user=user
        )

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()

    def test_post(self):
        client = Client()
        user = User.objects.get(name='아무개')
        token = jwt.encode({"user": user.id}, SECRET_KEY, ALGO)
        data = {
            "title": "제목1",
            "body": "내용1",
        }
        response = client.post('/post', json.dumps(data), content_type='application/json', **{"HTTP_Authorization": token})
        self.assertEqual(response.status_code, 201)
        post = Post.objects.get(title="제목1")
        self.assertEqual(response.json(), {"id": post.id, "title": data['title']})

    def test_fail_post(self):
        client = Client()
        data = {
            "title": "제목1",
            "body": "내용1",
        }
        response = client.post('/post', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
