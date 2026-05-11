from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from posts.models import Post, Comment, Group, Follow
from .serializers import (
    PostSerializer, CommentSerializer,
    GroupSerializer, FollowSerializer
)
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов (полный CRUD)"""
    queryset = Post.objects.all().order_by('-pub_date', 'id')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Только автор может редактировать пост')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Только автор может удалять пост')
        super
