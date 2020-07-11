# @Time    : 2020/07/02
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Article, ArticleDetail


class ArticleSerializer(serializers.ModelSerializer):
    """文章列表序列化类"""

    category = serializers.StringRelatedField(label='文章分类', read_only=True)

    class Meta:
        model = Article
        fields = ('title', 'summary', 'create_time', 'poll_count', 'category', 'comment_count', 'read_count')


class CreateArticleSerializer(serializers.ModelSerializer):
    """创建文章序列化类"""

    category_id = serializers.IntegerField(label='分类ID', write_only=True)
    content = serializers.CharField(label='文章内容', write_only=True)

    class Meta:
        model = Article
        fields = ('title', 'summary', 'status', 'stick', 'is_essence', 'category_id', 'content')

    def validate_title(self, attrs):
        try:
            title = Article.objects.get(title=attrs)
        except:
            title = None

        if title:
            raise serializers.ValidationError('此标题已存在！')
        return attrs

    def validate_category_id(self, attrs):
        try:
            category_id = Category.objects.get(id=attrs)
        except:
            category_id = None

        if not category_id:
            raise serializers.ValidationError('此分类标签不存在！')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        category = Category.objects.get(id=validated_data['category_id'])
        validated_data['category'] = category
        validated_data['user'] = user
        if not validated_data['summary']:
            validated_data['summary'] = validated_data['content'][:10] + '...'
        del validated_data['category_id']
        del validated_data['content']
        print(validated_data)
        article = super(CreateArticleSerializer, self).create(validated_data)
        print(article)
        ArticleDetail.objects.create(article_id=article.id, content=content)
        return article


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化类"""

    category = serializers.StringRelatedField(label='文章分类', read_only=True)
    user = serializers.StringRelatedField(label='作者', read_only=True)
    content = serializers.SerializerMethodField(label='展示用的文章内容')
    wirte_content = serializers.CharField(label='写入数据库的文章内容', write_only=True, allow_null=False)

    def get_content(self, instance):
        article_id = self.context['view'].kwargs['pk']
        try:
            content = ArticleDetail.objects.get(article_id=int(article_id)).content
        except:
            content = ''
        return content

    class Meta:
        model = Article
        fields = ('title', 'create_time', 'poll_count', 'category', 'comment_count',
                  'read_count', 'user', 'content', 'wirte_content')
        read_only_fields = ['read_count', 'comment_count', 'poll_count']

    def update(self, instance, validated_data):
        article_id = self.context['view'].kwargs['pk']
        try:
            article_detail = ArticleDetail.objects.get(article_id=int(article_id))
            article_detail.content = validated_data.get('wirte_content')
            article_detail.save()
        except:
            raise serializers.ValidationError('没有这篇文章')

        instance.title = validated_data.get('title')
        instance.save()
        return instance





