# @Time    : 2020/07/09
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, CommentPollViewSet

router = DefaultRouter()
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'comment_poll', CommentPollViewSet.as_view())

]