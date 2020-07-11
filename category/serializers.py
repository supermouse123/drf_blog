# @Time    : 2020/07/07
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from rest_framework import serializers
from blog.models import Category, Article

class CategorySerializer(serializers.ModelSerializer):
    """文章分类序列化类"""

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, attrs):
        try:
            name = Category.objects.get(name=attrs)
        except:
            name = None

        if name:
            raise serializers.ValidationError('此分类已存在！')
        return attrs


class CategoryDetailSerializer(serializers.ModelSerializer):
    """文章分类详情序列化类"""

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

