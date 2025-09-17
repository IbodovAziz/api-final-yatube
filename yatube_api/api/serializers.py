from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Group, Comment, Follow

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('id', 'author', 'created', 'post')


class FollowSerializer(serializers.ModelSerializer):
    """
    - user: (кто подписан)
    - following: (на кого подписан)
    """
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs.get('following')
        if user == following:
            raise serializers.ValidationError('Нельзя подписаться на себя.')

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError('Подписка уже существует.')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
