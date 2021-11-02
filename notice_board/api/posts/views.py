from django.views import View
from django.core.paginator import Paginator
from apps.posts.models import Post, Category, Comment, NestedComment, PostHits
from api.utils import LoginConfirm
import json
from django.http import JsonResponse, response
from datetime import date, datetime, timedelta, timezone


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        data = [{"id": instance.id, "name": instance.name} for instance in queryset]
        return JsonResponse(data={"data": data}, status=200)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        instance = Category.objects.create(name=data["name"])
        return JsonResponse(data={"id": instance.id, "name": instance.name}, status=201)


class PostView(View):
    @LoginConfirm
    def get(self, request, *args, **kwargs):
        if "post_id" in kwargs:
            try:
                instance = Post.objects.get(id=kwargs["post_id"])
            except Post.DoesNotExist:
                return JsonResponse(data={}, status=404)

            # 조회수 증가 - DB 이용 중복 제거
            if instance.user != request.user:
                if not PostHits.objects.filter(
                    user=request.user, post=instance
                ).exists():
                    PostHits.objects.create(
                        user=request.user, date=timezone.now(), post=instance
                    )
                    instance.hit += 1
                    instance.save()

            return JsonResponse(
                data={
                    "id": instance.id,
                    "title": instance.title,
                    "body": instance.body,
                    "category": instance.category,
                    "user": instance.user_id,
                    "hit": instance.hit,
                },
                status=200,
            )
        # 게시글 검색
        elif "keyword" in request.GET:
            queryset = Post.objects.filter(title__icontains=request.GET["keyword"])
        else:
            queryset = Post.objects.all()
        page_count = request.GET["page"] if request.GET.get("page") else 1
        pagination = Paginator(queryset, 25)
        page = pagination.get_page(page_count)
        data = {
            "data": [
                {
                    "id": instance.id,
                    "title": instance.title,
                    "body": instance.body,
                    "category": instance.category.name,
                }
                for instance in page.object_list
            ],
            "next": page.next_page_number() if page.has_next() else "",
            "previous": page.previous_page_number() if page.has_previous() else "",
            "count": len(page.object_list),
        }
        return JsonResponse(data=data, status=200)

    @LoginConfirm
    def post(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        data = json.loads(request.body)
        try:
            category = Category.objects.get(id=data["category"])
        except Category.DoesNotExist:
            return JsonResponse(data={}, status=400)

        instance = Post.objects.create(
            title=data["title"],
            body=data["body"],
            user=request.user,
            category=category,
        )
        return JsonResponse(
            data={"id": instance.id, "title": instance.title}, status=201
        )

    @LoginConfirm
    def patch(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        data = json.loads(request.body)
        try:
            instance = Post.objects.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            return JsonResponse(data={}, status=404)
        else:
            if instance.user != request.user:
                return JsonResponse(data={}, status=401)

        for key in data.keys():
            setattr(instance, key, data[key])

        instance.save()
        return JsonResponse(data={}, status=200)

    @LoginConfirm
    def delete(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        try:
            instance = Post.objects.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            return JsonResponse(data={}, status=404)
        else:
            if instance.user != request.user:
                return JsonResponse(data={}, status=401)

        instance.delete()
        return JsonResponse(data={}, status=204)


class CommentView(View):
    @LoginConfirm
    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            return JsonResponse(data={}, status=404)

        queryset = Comment.objects.filter(post=post)
        page_count = request.GET["page"] if request.GET.get("page") else 1
        pagination = Paginator(queryset, 25)
        page = pagination.get_page(page_count)
        data = {
            "data": [
                {
                    "id": instance.id,
                    "body": instance.body,
                    "post": instance.post_id,
                    "user": instance.user_id,
                }
                for instance in page.object_list
            ],
            "next": page.next_page_number() if page.has_next() else "",
            "previous": page.previous_page_number() if page.has_previous() else "",
            "count": len(page.object_list),
        }
        return JsonResponse(data=data, status=200)

    @LoginConfirm
    def post(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        data = json.loads(request.body)
        try:
            post = Post.objects.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            return JsonResponse(data={}, status=404)

        Comment.objects.create(post=post, body=data["body"], user=request.user)
        return JsonResponse(data={}, status=201)

    @LoginConfirm
    def patch(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        data = json.loads(request.body)
        try:
            instance = Comment.objects.get(id=kwargs["comment_id"])
        except Comment.DoesNotExist:
            return JsonResponse(data={}, status=404)
        else:
            if instance.user != request.user:
                return JsonResponse(data={}, status=401)

        for key in data.keys():
            setattr(instance, key, data[key])

        instance.save()
        return JsonResponse(data={}, status=200)

    @LoginConfirm
    def delete(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        try:
            instance = Comment.objects.get(id=kwargs["comment_id"])
        except Comment.DoesNotExist:
            return JsonResponse(data={}, status=404)
        else:
            if instance.user != request.user:
                return JsonResponse(data={}, status=401)

        instance.delete()
        return JsonResponse(data={}, status=204)


class NestedCommentView(View):
    @LoginConfirm
    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            return JsonResponse(data={}, status=404)

        try:
            comment = Comment.objects.get(id=kwargs["comment_id"])
        except Comment.DoesNotExist:
            return JsonResponse(data={}, status=404)

        queryset = NestedComment.objects.filter(post=post, comment=comment)
        page_count = request.GET["page"] if request.GET.get("page") else 1
        pagination = Paginator(queryset, 25)
        page = pagination.get_page(page_count)
        data = {
            "data": [
                {
                    "id": instance.id,
                    "body": instance.body,
                    "post": instance.post_id,
                    "comment": instance.comment_id,
                    "user": instance.user_id,
                }
                for instance in page.object_list
            ],
            "next": page.next_page_number() if page.has_next() else "",
            "previous": page.previous_page_number() if page.has_previous() else "",
            "count": len(page.object_list),
        }
        return JsonResponse(data=data, status=200)

    @LoginConfirm
    def post(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        data = json.loads(request.body)
        try:
            post = Post.objects.get(id=kwargs["post_id"])
        except Post.DoesNotExist:
            return JsonResponse(data={}, status=404)

        try:
            comment = Comment.objects.get(id=kwargs["comment_id"])
        except Comment.DoesNotExist:
            return JsonResponse(data={}, status=404)

        NestedComment.objects.create(
            post=post, comment=comment, user=request.user, body=data["body"]
        )
        return JsonResponse(data={}, status=201)

    @LoginConfirm
    def patch(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        data = json.loads(request.body)
        try:
            instance = NestedComment.objects.get(id=kwargs["nested_comment_id"])
        except NestedComment.DoesNotExist:
            return JsonResponse(data={}, status=404)
        else:
            if instance.user != request.user:
                return JsonResponse(data={}, status=401)

        for key in data.keys():
            setattr(instance, key, data[key])

        instance.save()
        return JsonResponse(data={}, status=200)

    @LoginConfirm
    def delete(self, request, *args, **kwargs):
        if request.user is None:
            return JsonResponse(data={}, status=401)

        try:
            instance = NestedComment.objects.get(id=kwargs["nested_comment_id"])
        except NestedComment.DoesNotExist:
            return JsonResponse(data={}, status=404)
        else:
            if instance.user != request.user:
                return JsonResponse(data={}, status=401)

        instance.delete()
        return JsonResponse(data={}, status=204)
