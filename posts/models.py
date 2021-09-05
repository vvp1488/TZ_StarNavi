from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    likes = GenericRelation('Like', related_name='posts')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_ad = models.DateTimeField(auto_now=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='objs')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
