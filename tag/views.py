# @Time    : 2020/07/15
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from .serializers import TagSerializer, ArticleTagRelationSerializer, TagDetailSerializer
from .models import ArticleTag, ArticleTagRelation
from blog.models import Article
from utils.custom import CustomPagination, CustomPermission


class TagViewSet(ModelViewSet):
    """文章标签视图类"""

    pagination_class = CustomPagination
    permission_classes = [CustomPermission]

    def get_queryset(self):
        if self.action == 'retrieve':
            tag_id = self.kwargs['pk']
            print(self.request.query_params)
            article_id_list = ArticleTagRelation.objects.filter(tag_id=tag_id).values_list('article')
            return Article.objects.filter(id__in=article_id_list)
        else:
            return ArticleTag.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TagDetailSerializer
        return TagSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)


class ArticleTagRelationViewSet(ModelViewSet):
    """文章标签对应关系视图类"""

    permission_classes = [CustomPermission]

    def get_queryset(self):
        return ArticleTagRelation.objects.all()

    def get_serializer_class(self):
        return ArticleTagRelationSerializer






