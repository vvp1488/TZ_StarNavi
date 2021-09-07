from time import timezone

from rest_framework import viewsets, permissions, status, generics, views
from rest_framework.response import Response

from .permissions import IsThisUserOrAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Post, Like, UserActivity
from .serializers import (
    PostSerializer,
    UserSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    PostCreateSerializer,
    LikeListSerializer,
    MyTokenObtainPairSerializer,
)
from .mixins import LikedMixin
from django.contrib.auth.models import User
from ..services import LikesFilter

from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PostViewSet(LikedMixin, viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        my_response_data = {**serializer.data, 'result': f'Пост создан'}
        serializer._data = my_response_data
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'posts_current_user' :
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrAdminOrReadOnly]
        else :
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        my_response_data = {**serializer.data, 'result': f'Пользователь создан'}
        serializer._data = my_response_data

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserDetailSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'result': f'Пользователь {instance.username} удален'}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsThisUserOrAdminOrReadOnly]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class LikeListAPI(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LikesFilter



