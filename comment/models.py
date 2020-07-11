# @Time    : 2020/07/09
# @Author  : sunyingqiang
# @Email   :  344670075@qq.com
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from blog.models import Article
# Create your models here.


class Comment(models.Model):
    """文章评论表"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    content = RichTextField('评论内容')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论用户')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论文章')
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE,
                                       verbose_name='父评论', related_name='parents')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "文章评论"
        verbose_name_plural = verbose_name


class CommentPoll(models.Model):
    """评论点赞表"""

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论文章')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞用户')

    class Meta:
        verbose_name = "评论点赞"
        verbose_name_plural = verbose_name

