from django.urls import path
from api.accounts.views import Signup, Login
from api.posts.views import PostView, CategoryView, CommentView, NestedCommentView

urlpatterns = [
    path("signup", Signup.as_view()),
    path("login", Login.as_view()),
    path("post", PostView.as_view()),
    path("post/<int:post_id>", PostView.as_view()),
    path("category", CategoryView.as_view()),
    path("post/<int:post_id>/comment", CommentView.as_view()),
    path("post/<int:post_id>/comment/<int:comment_id>", CommentView.as_view()),
    path(
        "post/<int:post_id>/comment/<int:comment_id>/big_comment",
        NestedCommentView.as_view(),
    ),
    path(
        "post/<int:post_id>/comment/<int:comment_id>/big_comment/<int:big_comment_id>",
        NestedCommentView.as_view(),
    ),
]
