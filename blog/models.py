# @Time    : 2020/07/02
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField
from db.base_model import BaseModel


class Category(models.Model):
    """文章分类模型类"""
    name = models.CharField(verbose_name='分类名', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name


class Article(BaseModel):
    """文章模型类"""
    PUBLISH_STATUS = (
        ('p', '文章页'),
        ('c', '教程页'),
        ('d', '草稿箱'),
        ('r', '回收站'),
    )

    STICK_STATUS = (
        ('y', '置顶'),
        ('n', '不置顶'),
    )
    title = models.CharField(verbose_name='标题', max_length=100)
    user = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    summary = models.CharField(verbose_name='摘要', max_length=200, blank=True)
    poll_count = models.IntegerField(verbose_name='点赞数', default=0)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    read_count = models.IntegerField(verbose_name='阅读量', default=0)
    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.CASCADE)
    status = models.CharField('文章状态', max_length=1, choices=PUBLISH_STATUS, default='p')
    stick = models.CharField('是否置顶', max_length=1, choices=STICK_STATUS, default='n')
    is_essence = models.BooleanField(verbose_name='是否精华', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    article_id = models.IntegerField(verbose_name='文章ID')
    content = MDTextField(verbose_name='正文')

    def __str__(self):
        return self.article_id

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name




