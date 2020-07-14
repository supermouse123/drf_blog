# @Time    : 2020/07/09
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment, CommentPoll
from blog.models import Article



class CommentSerializer(serializers.ModelSerializer):
    """文章评论序列化类"""

    user_id = serializers.StringRelatedField(label='用户id', read_only=True)
    article_id = serializers.StringRelatedField(label='评论文章id', read_only=True)
    comment_poll = serializers.SerializerMethodField(label='评论点赞数')

    def get_comment_poll(self, instance):
        count = CommentPoll.objects.filter(comment_id=instance.id).count()
        return count

    class Meta:
        model = Comment
        fields = ('create_time', 'content', 'user_id', 'article_id', 'comment_poll')


class SubCommentSerializer(serializers.ModelSerializer):
    """子评论序列化类"""

    user_id = serializers.StringRelatedField(label='用户id', read_only=True)
    article_id = serializers.StringRelatedField(label='评论文章id', read_only=True)
    parents = CommentSerializer(many=True, read_only=True)          #model里指定的related_name字段条件
    comment_poll = serializers.SerializerMethodField(label='评论点赞数')

    def get_comment_poll(self, instance):
        count = CommentPoll.objects.filter(comment_id=instance.id).count()
        return count

    class Meta:
        model = Comment
        fields = ('create_time', 'content', 'user_id', 'article_id', 'parents', 'comment_poll')


class CreateCommentSerializer(serializers.ModelSerializer):
    """创建评论序列化类"""

    user_id = serializers.CharField(label='用户名', allow_null=False, write_only=True)
    article_id = serializers.IntegerField(label='评论文章id', write_only=True)
    parent_comment = serializers.IntegerField(label='父级评论', allow_null=True, write_only=True)

    class Meta:
        model = Comment
        fields = ('content', 'user_id', 'article_id', 'parent_comment')


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user
        try:
            article = Article.objects.get(id=validated_data['article_id'])
            validated_data['article_id'] = article
        except:
            raise serializers.ValidationError('评论文章不存在!')
        if validated_data['parent_comment']:
            try:
                parent_comment = Comment.objects.get(id=validated_data['parent_comment'])
                validated_data['parent_comment'] = parent_comment
            except:
                raise serializers.ValidationError('上级评论不存在!')
        else:
            validated_data['parent_comment'] = None

        return super(CreateCommentSerializer, self).create(validated_data)






