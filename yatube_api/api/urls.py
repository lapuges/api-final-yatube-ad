from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follow')

# Комментарии — вложенный ресурс
comment_patterns = [
    path('', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', include((comment_patterns, 'comments'), namespace='comments')),
]