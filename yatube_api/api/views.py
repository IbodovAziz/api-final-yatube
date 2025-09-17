from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Api для постов."""
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Фильтр по группе (?group=ID). Пагинацию обрабатываем в list()."""
        qs = super().get_queryset()
        group_id = self.request.query_params.get('group')
        if group_id:
            qs = qs.filter(group_id=group_id)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        params = request.query_params
        if 'limit' in params or 'offset' in params:
            paginator = LimitOffsetPagination()
            page = paginator.paginate_queryset(qs, request, view=self)
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Api для групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    """Api для комментарий."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = None

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return Comment.objects.select_related('author', 'post').filter(
            post=self.get_post()
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Api для подписок."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)
    pagination_class = None

    def get_queryset(self):
        return Follow.objects.select_related('user', 'following').filter(
            user=self.request.user
        )
