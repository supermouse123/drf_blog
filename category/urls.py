# @Time    : 2020/07/07
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path(r'', include(router.urls)),

]