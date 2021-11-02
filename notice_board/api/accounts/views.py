import json

import jwt
from django.http import JsonResponse
from django.views import View

from apps.users.models import User
from notice_board.settings import SECRET_KEY, ALGO


class Signup(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if User.objects.filter(name=data['name']).exists():
            return JsonResponse(data={"message": "duplicate"}, status=400)

        User.objects.create(name=data["name"])
        return JsonResponse(data={"message": "user created"}, status=201)


class Login(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            instance = User.objects.get(name=data["name"])
        except User.DoesNotExist:
            return JsonResponse(data={}, status=400)

        token = jwt.encode({"user": instance.id}, SECRET_KEY, ALGO)
        return JsonResponse(data={"token": token}, status=200)
