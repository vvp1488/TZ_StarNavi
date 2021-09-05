from collections import OrderedDict

from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Post, Like
from .. import services as likes_services

from generic_relations.relations import GenericRelatedField
User = get_user_model()




class FanSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username'
        )


class PostSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'body',
            'is_fan',
            'total_likes',
            'owner',
        )

    def get_is_fan(self, obj):
        # Проверяем, лайкнул ли request.user пост obj
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class UserSerializer(serializers.ModelSerializer):

    posts = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'posts',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PostsCurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'total_likes'
        )
    #
    # def to_representation(self, instance):
    #     data = super(serializers.ModelSerializer, self).to_representation(instance)
    #     result = OrderedDict()
    #     result['data'] = data
    #     return result


class UserDetailSerializer(serializers.ModelSerializer):

    posts = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password' : { 'write_only' : True}
        }


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'total_likes'
        )


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password'
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'body',
        )

class PostSerializerForLike(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
        )

class LikeListSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    created_ad = serializers.DateTimeField(format="%Y-%m-%d")
    content_object = GenericRelatedField({
        Post: PostSerializerForLike()
    })

    class Meta:
        model = Like
        fields = (
            'id',
            'user',
            'created_ad',
            'content_object'

        )
    # user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    # created_ad = models.DateTimeField(auto_now=True, blank=True)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey()


