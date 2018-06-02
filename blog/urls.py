# coding=utf-8
from django.urls import path

from . import views


app_name = 'blog'
# 这里又踩了个坑，一定要用 path，不要用教程里的 url 函数，会有正则无法匹配的问题
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('category/<int:pk>/', views.category, name='category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),

    ]