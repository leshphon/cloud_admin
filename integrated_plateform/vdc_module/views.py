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

from django.conf import settings
from user_auth import models as auth_models
import models as vdc_models
# from api.keystone.test import vdc_user
import api.keystone.client as ksclient
import api.neutron.client as ntclient
import api.glance.client as gclient
import api.nova.client as nvclient


import utils


# ---------------manage user-----------------
def manage_user(request):
    user_lists = []
    user_role_obj = auth_models.User_Role_VDC.objects.filter(role_id=settings.SYSROLES['SYSUSER'])
    for i in user_role_obj:
        user_obj = i.user
        user_lists.append(user_obj)
    return render(request, 'vdc_module/module_user.html', {
        'user_lists': user_lists,
    })


def create_user(request):  # 前端提供的角色列表要加以限制，只能创建普通用户，即role_id=6
    utils.create_user_operation(request)
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
    if check_password(old_password, obj.password):  # 更改密码之前再次确认用户密码
        obj.password = make_password(new_password)
        obj.save()
    return HttpResponse('change passwd failed')


# ----------------instances manage---------------
def vdc_index(request):
    # openstack_user = request.session.get('openstack_user')
    recent_vdc_id = request.session.get('login_user_recent_vdc')
    user_role_id = request.session.get('login_role')
    user_name = request.session.get('username')

    user_obj = auth_models.User.objects.get(name__exact=user_name)
    vdc_obj = auth_models.VDC.objects.get(id=recent_vdc_id)
    role_obj = auth_models.Role.objects.get(id=user_role_id)

    # user_id = user_obj.id

    return render(request, 'vdc_module/index.html', {
        'error': 'here is error message',
        'currentpj': vdc_obj.name,
        'current_role_name': role_obj.name,
    })


def instance_index(request):
    # openstack_user = request.session.get('openstack_user')
    recent_vdc_id = request.session.get('login_user_recent_vdc')
    user_role_id = request.session.get('login_role')
    user_name = request.session.get('username')
    print(user_role_id)
    user_obj = auth_models.User.objects.get(name__exact=user_name)
    vdc_obj = auth_models.VDC.objects.get(id=recent_vdc_id)
    role_obj = auth_models.Role.objects.get(id=user_role_id)

    if user_role_id == settings.SYSROLES["SYSVDC"]:
        instance_obj = vdc_models.Server.objects.filter(created_in=recent_vdc_id)
    elif user_role_id == settings.SYSROLES["SYSUSER"]:
        instance_obj = vdc_models.Server.objects.filter(created_in=recent_vdc_id, created_by=user_obj.id)
    else:
        return HttpResponse(json.dumps({"error": "no this role!"}), content_type="application/json")
    ins_addr_list = []
    if instance_obj:
        for i in instance_obj:
            addr_obj = vdc_models.ServerAddresses.objects.filter(server_id=i.identification)
            ins_addr_list.append({"instance": i, "addr": addr_obj})
        return render(request, 'vdc_module/instance_index.html', {
            'currentpj': vdc_obj.name,
            'current_role_name': role_obj.name,
            'instance_params': ins_addr_list
        })
    else:
        return render(request, 'vdc_module/instance_index.html', {
            'currentpj': vdc_obj.name,
            'current_role_name': role_obj.name,
            'instance_params': ins_addr_list
        })


def instance_create(request):
    if request.method == "POST":
        openstack_user = request.session.get('openstack_user')
        # openstack_user = vdc_user
        result = nvclient.Client().create_servers(user=openstack_user, params=request.POST.get("data_body"))
        return HttpResponse(result)
    return render(request, 'vdc_module/instance_create.html')


def getStatusAction(request):
    openstack_user = request.session.get('openstack_user')
    user_role_id = request.session.get('login_role')
    if user_role_id == settings.SYSROLES["SYSVDC"]:
        flag = 1
    elif user_role_id == settings.SYSROLES["SYSUSER"]:
        flag = 0
    else:
        return HttpResponse(json.dumps({"error": "no this role!"}), content_type="application/json")
    return HttpResponse(
        json.dumps(nvclient.Client().check_action(user=openstack_user, status=request.POST.get("status"),
                                                  task_status=request.POST.get("task_status"),
                                                  role=user_role_id)), content_type="application/json"
    )


def updateServer(request):
    openstack_user = request.session.get('openstack_user')
    # user_role_id = request.session.get('login_role')

    result = nvclient.Client().update_servers(user=openstack_user,  params={"name": request.POST.get("name")},
                                              identification=request.POST.get("id"))
    return HttpResponse(result, content_type="application/json")



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
    openstack_user = request.session.get('openstack_user')
    result = nvclient.Client().show_flavor(user=openstack_user)
    return HttpResponse(result, content_type="application/json")


def flavor_create(request):
    openstack_user = request.session.get('openstack_user')
    if request.method == 'POST':
        result = nvclient.Client().create_flavor(user=openstack_user, params=request.POST.get("data_body"))
        return HttpResponse(result)
    return render(request, 'vdc_module/flavor_create.html')


# def show_image(request):
#     result = glanceclient.image.show(user=request.session.get("user"), image_id=None, value=None)
#     return HttpResponse(result, content_type="application/json")

# def instance_build_type(request):
#     return render(request, 'vdc_module/vdc_instance_build_type.html')


# ---------------network-manage--------------------------
def network_manage(request):
    return render(request, 'vdc_module/vdc_network_manage.html')


def route_manage(request):
    return render(request, 'vdc_module/vdc_route_manage.html')
