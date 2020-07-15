# @Time    : 2020/07/15
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.db import models
from blog.models import Article

# Create your models here.


class ArticleTag(models.Model):
    """文章标签模型类"""

    name = models.CharField(verbose_name='标签名', max_length=50)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name


class ArticleTagRelation(models.Model):
    """文章标签对应关系模型类"""

    tag_id = models.IntegerField(verbose_name='标签id')
    article = models.IntegerField(verbose_name='文章id')

    class Meta:
        verbose_name = '文章标签关系'
        verbose_name_plural = verbose_name
