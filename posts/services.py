from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like
from django_filters import rest_framework as filters
User = get_user_model()


def add_like(obj, user):

    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):

    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_fan(obj, user):
    # Проверяем лайкнул ли user данный obj
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    # Получаем всех пользователей,которые лайкнули obj
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)


class LikesFilter(filters.FilterSet):
    #
    created_ad = filters.DateFromToRangeFilter()

    class Meta:
        model = Like
        # fields = {
        #     'created_ad': ['lte', 'gte'],
        # }
        fields = (
            'created_ad',
        )