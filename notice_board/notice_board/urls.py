from django.urls import path
from api.accounts.views import Signup, Login

urlpatterns = [
    path("signup", Signup.as_view()),
    path("login", Login.as_view()),
]
