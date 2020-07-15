# @Time    : 2020/07/14
# @Author  : sunyingqiang
# @Email   : 344670075@qq.com
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path(r'', include(router.urls)),

]