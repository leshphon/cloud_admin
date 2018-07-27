# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from vdc_module.api.member import User, Token, Domain
import vdc_module.api.keystone.interface as keystoneclient
import vdc_module.api.nova.interface as novaclient

import vdc_module.api.glance.interface as glanceclient
import json


import vdc_module.api.neutron.interface as neutronclient

from user_auth import models as auth_models
import models

from django.shortcuts import redirect
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.conf import settings
# Create your views here.

#---------------manage user-----------------
def manage_user(request):
    user_lists = []
    user_role_obj = auth_models.User_Role_VDC.objects.filter(role_id=settings.SYSROLES['SYSUSER'])
    for i in user_role_obj:
        user_obj = i.user
        user_lists.append(user_obj)
    return render(request, 'vdc_module/vdc_module_user.html', {
        'user_lists': user_lists,
    })

def create_user(request):                 #前端提供的角色列表要加以限制，只能创建普通用户，即role_id=6
    models.create_user_operation(request)
    # 返回的是user_role_vdc里的一个对象
    return redirect('/vdc_manage_user')

def del_user(request):
    user_id = request.GET.get('id')
    auth_models.User.objects.filter(id=user_id).delete()
    return redirect('/vdc_manage_user')

def update_user(request):
    param = request.GET.get("data")
    print(param)
    update_info = json.loads(param)
    print('123:', update_info)
    print('123:', update_info['user_id'])
    user_id = update_info['user_id']
    name = update_info['name']
    email = update_info['email']
    auth_models.User.objects.filter(id=user_id).update(name=name, email=email)
    return HttpResponse('ok')

def change_user_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    user_id = request.POST.get('user_id')
    obj = auth_models.User.objects.get(id=user_id)
    if check_password(old_password,obj.password):    #更改密码之前再次确认用户密码
        obj.password = make_password(new_password)
        obj.save()
    return HttpResponse('change passwd failed')



#----------------instance...manage---------------
def vdc_index(request):
    return render(request, 'vdc_module/vdc_index.html', {
        'error': 'here is error message',
    })


def instance_manage(request):
    openstack_login(request)
    user = request.session.get('user')
    return render(request, 'vdc_module/vdc_instance_manage.html', {
        'currentpj': user.project.currentpj,
        'current_role_name': user.role.current_role_name
    })


def instance_create(request):
    return render(request, 'vdc_module/vdc_create_instance.html')


def create_server(request):
    user = request.session.get("user")
    info = request.POST.get("data_body")
    # info = request.body
    # print(info)
    # print(info)
    result = novaclient.server.create(user, info)
    return HttpResponse(result)


def openstack_login(request):
    unscoped_user = User(username='admin', password='admin', domain=Domain(current_domain="Default"))
    scoped_user = keystoneclient.pwd_login(unscoped_user)
    print scoped_user.token
    print('login')
    if scoped_user is None:
        return HttpResponse('用户名或密码错误')
    # Set session
    request.session['user'] = scoped_user


def show_server(request):
    result = novaclient.server.show(user=request.session.get("user"))
    return HttpResponse(result, content_type="application/json")


def showNet(request):
    openstack_login(request)
    result = neutronclient.networks.show(user=request.session.get("user"))
    print(result)
    return HttpResponse(result, content_type="application/json")


def show_flavors(request):
    result = novaclient.flavor.show(user=request.session.get("user"), flavor_id=None)
    return HttpResponse(result, content_type="application/json")


def show_image(request):
    result = glanceclient.image.show(user=request.session.get("user"), image_id=None, value=None)
    return HttpResponse(result, content_type="application/json")


def show_keypairs(request):
    result = novaclient.keypairs.show(user=request.session.get("user"))
    return HttpResponse(result, content_type="application/json")


def getStatusAction(request):
    return HttpResponse(
        json.dumps(novaclient.server.status.checkAction(user=request.session.get("user"))),
        content_type="application/json"
    )


def pauseServer(request):
    result = novaclient.server.pause(user=request.session.get("user"), server_id=request.POST.get('server_id'))
    return HttpResponse(result, content_type="application/json")


def unpauseServer(request):
    item_id = request.POST.get('server_id')
    result = novaclient.server.unpause(user=request.session.get("user"), server_id=item_id)
    return HttpResponse(result, content_type="application/json")


def suspendServer(request):
    # if request.is_ajax() and request.method == 'POST':
    result = novaclient.server.suspend(user=request.session.get("user"), server_id=request.POST.get('server_id'))
    return HttpResponse(result, content_type="application/json")


def unsuspendServer(request):
    # if request.is_ajax() and request.method == 'POST':
    result = novaclient.server.unsuspend(user=request.session.get("user"), server_id=request.POST.get('server_id'))
    return HttpResponse(result, content_type="application/json")


def deleteServer(request):
    # if request.is_ajax() and request.method == 'POST':
    server_id = request.POST.get('server_id')
    result = novaclient.server.delete(user=request.session.get("user"), server_id=server_id)
    # return HttpResponse(result, content_type="application/json")
    return HttpResponse(result)


def showSingleSever(request):
    item_id = request.POST.get('server_id')
    result = novaclient.server.details(user=request.session.get("user"), server_id=item_id)
    return HttpResponse(result, content_type="application/json")


def instance_type(request):
    return render(request, 'vdc_module/vdc_instance_type.html')


def instance_build_type(request):
    return render(request, 'vdc_module/vdc_instance_build_type.html')


#---------------network-manage--------------------------
def network_manage(request):
    return render(request, 'vdc_module/vdc_network_manage.html')

def route_manage(request):
    return render(request, 'vdc_module/vdc_route_manage.html')

