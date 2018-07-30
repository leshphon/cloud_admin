# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'user_auth'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^login_test', views.login_test, name='login_test'),
]
