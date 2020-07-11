# @Time    : 2020/07/02
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from .serializers import ArticleSerializer, CreateArticleSerializer, \
    ArticleDetailSerializer
from .models import Article, Category
from utils.custom import CustomPermission, CustomPagination


class ArticleViewSet(ModelViewSet):
    """文章视图类"""

    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'poll_count', 'comment_count', 'read_count')
    permission_classes = [CustomPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        elif self.action == 'create':
            return CreateArticleSerializer
        else:
            return ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=int(self.kwargs['pk']))
            article.read_count += 1
            article.save()
        except:
            return Response({'message': '文章不存在'})
        return super(ArticleViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=int(self.kwargs['pk']))
            if article.user != request.user:
                raise
        except:
            return Response({'message': '用户无权删除'})
        return super(ArticleViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(id=int(self.kwargs['pk']))
            if article.user != request.user:
                raise
        except:
            return Response({'message': '用户无权修改'})
        return super(ArticleViewSet, self).update(request, *args, **kwargs)


class ArticlePollView(APIView):
    """文章点赞视图类"""

    permission_classes = [CustomPermission]

    def post(self, request):
        article_id = request.data['article_id']
        conn = get_redis_connection('default')
        username = request.user

        try:
            article = Article.objects.get(id=article_id)
            user_in_redis = conn.sismember('poll_article_%s' % (article_id), 'user_%s' % (username))
            if not user_in_redis:
                article.poll_count += 1
                article.save()
                conn.sadd('poll_article_%s' % (article_id), 'user_%s' % (username))
            else:
                return Response({'message': '该用户已点赞过这篇文章'})
        except:
            return Response({'message': '没有这篇文章'})
        return Response({'message': '点赞成功'})

    def put(self, request):
        article_id = request.data['article_id']
        conn = get_redis_connection('default')
        username = request.user
        try:
            article = Article.objects.get(id=article_id)
            user_in_redis = conn.sismember('poll_article_%s' % (article_id), 'user_%s' % (username))
            if user_in_redis:
                article.poll_count -= 1
                article.save()
                conn.srem('poll_article_%s' % (article_id), 'user_%s' % (username))
            else:
                return Response({'message': '该用户没有点赞过这篇文章!'})
        except:
            return Response({'message': '没有这篇文章'})
        return Response({'message': '取消点赞'})





