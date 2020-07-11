# @Time    : 2020/07/09
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, SubCommentSerializer, CreateCommentSerializer
from blog.models import Article


class CommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,GenericViewSet):
    """用户评论视图类"""

    def get_queryset(self):
        try:
            article_id = self.request.query_params['article_id']
            try:
                article = Article.objects.get(id=article_id)
                if self.action == 'list':
                    return Comment.objects.filter(parent_comment=None, article_id=article)
                else:
                    return Comment.objects.filter(article_id=article)
            except:
                return None
        except:
            if self.action == 'list':
                return Comment.objects.filter(parent_comment=None)
            else:
                return Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        elif self.action == 'retrieve':
            return SubCommentSerializer
        else:
            return CreateCommentSerializer

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response({'message': '没有这篇文章'})
        else:
            return super(CommentViewSet, self).list(request, *args, **kwargs)

