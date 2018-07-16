# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'system_module'

urlpatterns = [
    url(r'^index', views.sys_index, name='sys_index'),
    url(r'^manage_vdc', views.manage_vdc, name='manage_vdc'),
    url(r'^manage_user', views.manage_user, name='manage_user'),
    url(r'^manage_role', views.manage_role, name='manage_role'),
    url(r'^create_user', views.create_user, name='create_user'),
    url(r'^create_vdc$', views.create_vdc, name='create_vdc'),
    url(r'^create_vdc_admin$', views.create_vdc_admin, name='create_vdc_admin'),
    url(r'^get_quota$', views.get_quota, name='get_quota'),
    url(r'^del_user$', views.del_user, name='del_user'),
]