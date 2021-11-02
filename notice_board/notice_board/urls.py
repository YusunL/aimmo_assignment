from django.urls import path
from api.accounts.views import Signup, Login
from api.posts.views import PostView

urlpatterns = [
    path("signup", Signup.as_view()),
    path("login", Login.as_view()),
    path("post", PostView.as_view()),
    path("post/<int:post_id>", PostView.as_view()),
]
