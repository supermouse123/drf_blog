# @Time    : 2020/07/02
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ArticlePollView

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'poll', ArticlePollView.as_view())

]