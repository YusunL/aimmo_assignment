from django.views import View
from django.core.paginator import Paginator
from apps.posts.models import Post
from api.utils import LoginConfirm
import json
from django.http import JsonResponse


class PostView(View):
    @LoginConfirm
    def get(self, request, *args, **kwargs):
        if "post_id" in kwargs:
            try:
                instance = Post.objects.get(id=kwargs["post_id"])
            except Post.DoesNotExist:
                return JsonResponse(data={}, status=404)

            return JsonResponse(
                data={
                    "id": instance.id,
                    "title": instance.title,
                    "body": instance.body,
                    "user": instance.user_id,
                },
                status=200,
            )
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

        instance = Post.objects.create(
            title=data["title"],
            body=data["body"],
            user=request.user,
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
            if instance.writer != request.user:
                return JsonResponse(data={}, status=401)

        instance.delete()
        return JsonResponse(data={}, status=204)
