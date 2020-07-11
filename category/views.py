# @Time    : 2020/07/07
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import serializers

from blog.models import Category, Article
from .serializers import CategorySerializer, CategoryDetailSerializer
from utils.custom import CustomPermission, CustomPagination


class CategoryViewSet(ModelViewSet):
    """文章分类视图类"""

    permission_classes = [CustomPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.action == 'retrieve':
            category_id = self.kwargs['pk']
            try:
                category = Category.objects.get(id=category_id)
                return Article.objects.filter(category=category)
            except:
                return None
        else:
            return Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        else:
            return CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if not instance:
            return Response({'message': '没有这个分类！'})
        serializer = self.get_serializer(page, many=True)
        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):

            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
