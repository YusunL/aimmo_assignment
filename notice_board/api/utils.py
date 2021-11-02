import jwt
from django.http import JsonResponse
from apps.users.models import User
from notice_board.settings import SECRET_KEY, ALGO


class LoginConfirm:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, ALGO)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message": "EXPIRED_TOKEN"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"message": "INVALID_JWT"}, status=401)

            try:
                user = User.objects.get(id=payload["user"])
            except User.DoesNotExist:
                return JsonResponse({"message": "NEED_LOGIN"}, status=401)

            request.user = user
            return self.func(self, request, *args, **kwargs)
        else:
            request.user = None
            return self.func(self, request, *args, **kwargs)
