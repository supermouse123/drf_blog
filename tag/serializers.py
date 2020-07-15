# @Time    : 2020/07/15
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework import serializers
from .models import ArticleTag, ArticleTagRelation
from blog.models import Article


class TagSerializer(serializers.ModelSerializer):
    """标签序列化类"""

    class Meta:
        model = ArticleTag
        fields = '__all__'

    def validate_name(self, attrs):
        print(attrs)
        try:
            name = ArticleTag.objects.get(name=attrs)
        except:
            name = None

        if name:
            raise serializers.ValidationError('标签名已存在')
        return attrs


class ArticleTagRelationSerializer(serializers.ModelSerializer):
    """文章标签关系序列化类"""

    class Meta:
        model = ArticleTagRelation
        fields = '__all__'

    def validate_tag_id(self, attrs):
        print(attrs)
        try:
            tag_id = ArticleTag.objects.get(id=attrs)
        except:
            tag_id = None

        if not tag_id:
            raise serializers.ValidationError('标签名不存在')
        return attrs

    def validate_article(self, attrs):
        print(attrs)
        try:
            article_id = Article.objects.get(id=attrs)
        except:
            article_id = None

        if not article_id:
            raise serializers.ValidationError('文章不存在')
        return attrs

    def validate(self, attrs):
        article_id = attrs['article']
        tag_id = attrs['tag_id']
        try:
            relation = ArticleTagRelation.objects.get(article=article_id, tag_id=tag_id)
        except:
            relation = None

        if relation:
            raise serializers.ValidationError('这篇文章已存在这个标签，请勿重复选择')
        return attrs

    def create(self, validated_data):
        article_count = ArticleTagRelation.objects.filter(article=validated_data['article']).count()
        if article_count == 3:
           raise serializers.ValidationError('每篇文章最多三个标签')
        print(article_count)
        return super(ArticleTagRelationSerializer, self).create(validated_data)


class TagDetailSerializer(serializers.ModelSerializer):
    """文章标签详情序列化类"""

    category = serializers.StringRelatedField(label='文章分类', read_only=True)
    url = serializers.SerializerMethodField(label='url')

    def get_url(self, instance):
        print(instance)
        path = self.context['request'].META['HTTP_HOST']
        url = 'http://' + path + '/api/article/' + str(instance.id)
        return url

    class Meta:
        model = Article
        fields = ('title', 'summary', 'create_time', 'poll_count', 'category', 'comment_count', 'read_count', 'url')

