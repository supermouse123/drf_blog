# @Time    : 2020/07/15
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, ArticleTagRelationViewSet

router = DefaultRouter()
router.register('tag', TagViewSet, basename='tag')
router.register('tagrelation', ArticleTagRelationViewSet, basename='tagrelation')

urlpatterns = [
    path(r'', include(router.urls)),


]