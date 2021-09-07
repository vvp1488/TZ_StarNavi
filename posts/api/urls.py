from django.contrib.contenttypes.models import ContentType
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView

model = ContentType

from .views import PostViewSet, UserViewSet, LikeListAPI, UserActivityList

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view()),
    path('analitics/', LikeListAPI.as_view()),
    path('user_activity/', UserActivityList.as_view())


]
urlpatterns += router.urls