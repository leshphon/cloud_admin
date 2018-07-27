# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'user_auth'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'test_', views.login2, name='login2'),
    url(r'^logout', views.logout, name='logout'),
]
