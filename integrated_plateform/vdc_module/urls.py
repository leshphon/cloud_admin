# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'vdc_module'

urlpatterns = [
    url(r'^index', views.vdc_index, name='vdc_index'),
    url(r'^instance_manage', views.instance_manage, name='instance_manage'),
    url(r'^create_server', views.create_server, name='create_server'),
    url(r'^show_server', views.show_server, name='show_server'),
    url(r'^getStatusAction', views.getStatusAction, name='getStatusAction'),
    url(r'^pauseServer', views.pauseServer, name='pauseServer'),
    url(r'^unpauseServer', views.unpauseServer, name='unpauseServer'),
    url(r'^suspendServer', views.suspendServer, name='suspendServer'),
    url(r'^unsuspendServer', views.unsuspendServer, name='unsuspendServer'),
    url(r'^deleteServer', views.deleteServer, name='deleteServer'),
    url(r'^showSingleSever', views.showSingleSever, name='showSingleSever'),
    url(r'^instance_create', views.instance_create, name='instance_create'),
    url(r'^show_net', views.showNet, name='vdc_show_net'),
    url(r'^show_flavors', views.show_flavors, name='show_flavors'),
    url(r'^show_image', views.show_image, name='show_image'),
    url(r'^show_keypairs', views.show_keypairs, name='show_keypairs'),
]
