# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from utils import sync_database_all

app_name = 'vdc_module'

urlpatterns = [
    url(r'^index', views.vdc_index, name='vdc_index'),
    url(r'^instance_index', views.instance_index, name='instance_index'),
    url(r'^instance_create', views.instance_create, name='instance_create'),
    # url(r'^instance_show', views.instance_show, name='instance_show'),

    url(r'^getStatusAction', views.getStatusAction, name='getStatusAction'),
    url(r'^updateServer', views.updateServer, name='updateServer'),
    # url(r'^pauseServer', views.pauseServer, name='pauseServer'),
    # url(r'^unpauseServer', views.unpauseServer, name='unpauseServer'),
    # url(r'^suspendServer', views.suspendServer, name='suspendServer'),
    # url(r'^unsuspendServer', views.unsuspendServer, name='unsuspendServer'),
    # url(r'^deleteServer', views.deleteServer, name='deleteServer'),
    # url(r'^showSingleSever', views.showSingleSever, name='showSingleSever'),

    # url(r'^show_net', views.showNet, name='vdc_show_net'),
    url(r'^flavor_index', views.flavor_index, name='flavor_index'),
    url(r'^flavor_show', views.flavor_show, name='flavor_show'),
    url(r'^flavor_create', views.flavor_create, name='flavor_create'),
    # url(r'^show_image', views.show_image, name='show_image'),
    # url(r'^show_keypairs', views.show_keypairs, name='show_keypairs'),
    # url(r'^instance_type', views.instance_type, name='instance_type'),
    # url(r'^instance_build_type', views.instance_build_type, name='instance_build_type'),

    url(r'^network_manage',views.network_manage,name="network_manage"),
    url(r'^route_manage', views.route_manage, name="route_manage"),

    url(r'^manage_user', views.manage_user, name='manage_user'),
    url(r'^create_user', views.create_user, name='create_user'),
    url(r'^delete_user$', views.del_user, name='delete_user'),
    url(r'^update_user$', views.update_user, name='update_user'),
]


sync_database_all()