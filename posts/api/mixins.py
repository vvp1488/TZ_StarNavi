from collections import OrderedDict

from rest_framework.response import Response

from .. import services
from rest_framework.decorators import action
from posts.api.serializers import (
    FanSerializer,
    PostsCurrentUserSerializer,
    LikeSerializer,
)
from posts.models import Post
from django.contrib.auth.models import User


class LikedMixin:

    @action(methods=['POST'], detail=True)
    def like(self,request, pk=None):
        # Лайкаем obj
        obj = self.get_object()

        post = Post.objects.filter(id=self.kwargs['pk']).first()
        serializer = LikeSerializer(post)
        if services.is_fan(obj,request.user):
            my_response_data = {**serializer.data, 'result': f'Пользователь {request.user} лайкал уже этот пост'}
        else:
            services.add_like(obj, request.user)
            my_response_data = {**serializer.data, 'result': f'Пользователь {request.user} поставил лайк'}
        serializer._data = my_response_data
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def unlike(self, request, pk=None):
        # Удаляем лайк с obj
        obj = self.get_object()
        post = Post.objects.filter(id=self.kwargs['pk']).first()
        serializer = LikeSerializer(post)
        if services.is_fan(obj,request.user):
            services.remove_like(obj, request.user)
            my_response_data = {**serializer.data, 'result': f'Пользователь {request.user} убрал лайк'}
        else:
            my_response_data = {**serializer.data, 'result': f'Пользователь {request.user} не лайкал эту запись'}
        serializer._data = my_response_data
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def fans(self, request, pk=None):
        # Получаем всех пользователей которые лайкнули obj
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def posts_current_user(self, request):
        user = User.objects.get(username=request.user.username)
        posts = user.posts.all()
        serializer = PostsCurrentUserSerializer(posts, many=True)
        return Response(OrderedDict(
            [
                ("total_posts", posts.count()),
                ("results", serializer.data)
            ]
        ))




