# coding=utf-8
from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag


register = template.Library()


# 为了能够通过 {% get_recent_posts %} 的语法在模板中调用这个函数，必须按照 Django 的规定注册这个函数为模板标签，
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    # created_time ，即Post的创建时间，month是精度，order = 'DESC' 表明降序排列（即离当前越近的时间越排在前面）
    # 例如我们写了3篇文章，分别发布于2017年2月21日、2017年3月25日、2017年3月28日，
    # 那么dates函数将返回2017年3月和2017年2月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。
    return Post.objects.dates('created_time', 'month', order='DESC')


# @register.simple_tag
# def get_category():
#     return Category.objects.all()


@register.simple_tag
def get_categories():
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


