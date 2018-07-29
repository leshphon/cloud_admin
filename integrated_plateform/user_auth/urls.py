# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'user_auth'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
]
