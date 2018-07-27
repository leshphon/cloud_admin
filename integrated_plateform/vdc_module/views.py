# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
import json

from user_auth import models as auth_models
import models as vdc_models
from api.keystone.test import vdc_user
import api.keystone.client as ksclient
import api.neutron.client as ntclient
import api.glance.client as gclient
import api.nova.client as nvclient

import utils


# ---------------manage user-----------------
def manage_user(request):
    exclude = ['id', 'password', 'created_time', 'updated_time', 'status', 'recent_use_VDC', 'cpu', 'ram', 'volume',
               'instances', 'used_ram', 'used_cpu', 'used_volume', 'used_instances']
    print_user_fields = utils.print_fields(exclude, 'User')
    user_lists = []
    # user_role_list = []                 #用户的角色列表
    user_role_obj = auth_models.User_Role_VDC.objects.all()
    for i in user_role_obj:
        if i.role_id == settings.SYSROLES['SYSUSER'] and i.vdc_id == request.session['login_user_recent_vdc']:    #判断是登录vdc_admin_user所管理的vdc中的用户
            print('333333333333:',request.session['login_user_recent_vdc'],i.vdc_id)
            user_obj = i.user
            user_lists.append(user_obj)
    print("this is vdc user list:",user_lists)
    return render(request, 'vdc_module/module_user.html', {
        'user_fields': print_user_fields,
        'user_lists': user_lists,
    })


def create_user(request):  # 前端提供的角色列表要加以限制，只能创建普通用户，即role_id=6
    utils.create_user_operation(request)
    # 返回的是user_role_vdc里的一个对象
    return redirect('/sys_manage_user')


def del_user(request):
    user_id = request.POST.get('user_id')
    print(user_id)
    auth_models.User.objects.filter(id=user_id).delete()
    return redirect('/sys_manage_user')


def update_user(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('username')
    email = request.POST.get('email')
    auth_models.User.objects.filter(id=user_id).update(name=name, email=email)


def change_user_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    user_id = request.POST.get('user_id')
    obj = auth_models.User.objects.get(id=user_id)
    if check_password(old_password, obj.password):  # 更改密码之前再次确认用户密码
        obj.password = make_password(new_password)
        obj.save()
    return HttpResponse('change passwd failed')


# ----------------instances manage---------------
def vdc_index(request):
    return render(request, 'vdc_module/index.html', {
        'error': 'here is error message',
    })


def instance_index(request):
    # openstack_user = request.session.get('openstack_user')
    # recent_vdc_id = request.session.get('recent_vdc')
    # user_role_id = request.session.get('user_role')
    # user_id = request.session.get('user')
    openstack_user = vdc_user
    recent_vdc_id = 15
    user_role_id = 6
    user_id = 4

    vdc_obj = auth_models.VDC.objects.filter(id=recent_vdc_id)
    role_obj = auth_models.Role.objects.filter(id=user_role_id)
    if user_role_id == 1:
        instance_obj = vdc_models.Server.objects.filter(created_in=recent_vdc_id)
    elif user_role_id == 6:
        instance_obj = vdc_models.Server.objects.filter(created_in=recent_vdc_id, created_by=str(user_id))
    else:
        print("auth error!")
        return

    ins_addr_list = []
    for i in instance_obj:
        addr_obj = vdc_models.ServerAddresses.objects.filter(server_id=i.identification)
        ins_addr_list.append({"instance": i, "addr": addr_obj})
    return render(request, 'vdc_module/instance_index.html', {
        'currentpj': vdc_obj[0].name,
        'current_role_name': role_obj[0].name,
        'instance_params': ins_addr_list

    })


def instance_create(request):
    if request.method == "POST":
        # openstack_user = request.session.get('openstack_user')
        openstack_user = vdc_user
        result = nvclient.Client().create_servers(user=openstack_user, params=request.POST.get("data_body"))
        return HttpResponse(result)
    return render(request, 'vdc_module/instance_create.html')


def instance_show(request):
    # openstack_user = request.session.get('openstack_user')
    openstack_user = vdc_user
    if not request.POST.get("id"):
        result = nvclient.Client().show_servers(user=openstack_user)
    else:
        result = nvclient.Client().show_servers(user=openstack_user, identification=request.POST.get("id"))
    print result
    return HttpResponse(result, content_type="application/json")


def getStatusAction(request):
    # openstack_user = request.session.get('openstack_user')
    openstack_user = vdc_user
    return HttpResponse(
        json.dumps(nvclient.Client().check_action(user=openstack_user)),
        content_type="application/json"
    )


# def showNet(request):
#     result = neutronclient.networks.show(user=request.session.get("user"))
#     return HttpResponse(result, content_type="application/json")
#
#

#
# def show_keypairs(request):
#     result = novaclient.keypairs.show(user=request.session.get("user"))
#     return HttpResponse(result, content_type="application/json")
#
#


# def pauseServer(request):
#     result = novaclient.server.pause(user=request.session.get("user"), server_id=request.POST.get('server_id'))
#     return HttpResponse(result, content_type="application/json")
#
#
# def unpauseServer(request):
#     item_id = request.POST.get('server_id')
#     result = novaclient.server.unpause(user=request.session.get("user"), server_id=item_id)
#     return HttpResponse(result, content_type="application/json")
#
#
# def suspendServer(request):
#     # if request.is_ajax() and request.method == 'POST':
#     result = novaclient.server.suspend(user=request.session.get("user"), server_id=request.POST.get('server_id'))
#     return HttpResponse(result, content_type="application/json")
#
#
# def unsuspendServer(request):
#     # if request.is_ajax() and request.method == 'POST':
#     result = novaclient.server.unsuspend(user=request.session.get("user"), server_id=request.POST.get('server_id'))
#     return HttpResponse(result, content_type="application/json")
#
#
# def deleteServer(request):
#     # if request.is_ajax() and request.method == 'POST':
#     server_id = request.POST.get('server_id')
#     result = novaclient.server.delete(user=request.session.get("user"), server_id=server_id)
#     # return HttpResponse(result, content_type="application/json")
#     return HttpResponse(result)
#
#
# def showSingleSever(request):
#     item_id = request.POST.get('server_id')
#     result = novaclient.server.details(user=request.session.get("user"), server_id=item_id)
#     return HttpResponse(result, content_type="application/json")

def flavor_index(request):
    return render(request, 'vdc_module/flavor_index.html')


def flavor_show(request):
    # openstack_user = request.session.get('openstack_user')
    openstack_user = vdc_user
    result = nvclient.Client().show_flavor(user=openstack_user)
    return HttpResponse(result, content_type="application/json")


def flavor_create(request):
    # openstack_user = request.session.get('openstack_user')
    openstack_user = vdc_user
    if request.method == 'POST':
        result = nvclient.Client().create_flavor(user=openstack_user, params=request.POST.get("data_body"))
        return HttpResponse(result)
    return render(request, 'vdc_module/flavor_create.html')

# def show_image(request):
#     result = glanceclient.image.show(user=request.session.get("user"), image_id=None, value=None)
#     return HttpResponse(result, content_type="application/json")
