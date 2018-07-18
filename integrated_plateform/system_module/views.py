# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from user_auth import models as auth_models
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.apps import apps
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
import json
from django.core import serializers
from user_auth.views import auth
import models


# Create your views here.
def sys_index(request):
    return render(request, 'system_module/sys_index_overview.html')


#-----------manage VDC---------------
@auth
def manage_vdc(request):
    exclude = ['created_time', 'backend_info', 'usage']
    print_vdc_fields = models.print_fields(exclude,'VDC')
    vdc_lists = auth_models.VDC.objects.all()
    vdc_admins_obj = auth_models.User_Role_VDC.objects.filter(role_id=3)
    vdc_admins = []
    for i in vdc_admins_obj:
        if i.vdc_id == None:        #判断该用户是否已经是某个vdc的管理员了
            vdc_admins.append(auth_models.User.objects.get(id=i.user_id))
    return render(request, 'system_module/sys_manage_vdc.html', {
        'vdc_fields': print_vdc_fields,
        'vdc_lists': vdc_lists,
        'vdc_admins': vdc_admins,
    })

def create_vdc(request):
    name = request.POST.get('vdc_name')
    desc = request.POST.get('vdc_desc')
    vdc_admin_id = request.POST.get('vdc_admin_id')
    quota_obj = models.quota_create(request)
    vdc_obj = auth_models.VDC(name=name, description=desc, quota_id=quota_obj.id)
    vdc_obj.save()
    user_vdc_obj = auth_models.User_Role_VDC(vdc_id=vdc_obj.id,user_id=vdc_admin_id,role_id=3)
    user_vdc_obj.save()
    return redirect('/sys_manage_vdc')

#创建vdc时，选择新建一个用户作为vdc管理员
def create_vdc_admin(request):
    models.create_user_operation(request)
    return HttpResponse(serializers.serialize('json', [auth_models.User.objects.get(name=request.POST.get('username'))]))
    # return HttpResponse('ok')

def get_quota(request):
    quota_id = request.POST.get('quota_id')
    print(quota_id)
    quota_detail = auth_models.Quota.objects.get(id__exact=quota_id)
    return HttpResponse(serializers.serialize('json', [quota_detail]), content_type="application/json")

def del_VDC(request):
    vdc_id = request.POST.get('vdc_id')
    auth_models.VDC.objects.filter(id=vdc_id).delete()
    return redirect('/sys_manage_vdc')

def update_VDC(request):
    vdc_id = request.POST.get('vdc_id')
    name = request.POST.get('update_name')
    desc = request.POST.get('update_desc')
    auth_models.VDC.objects.filter(id=vdc_id).update(name=name,description=desc)

#------------manage user-------------
@auth
def manage_user(request):
    exclude = ['password', 'created_time', 'status', 'recent_use_VDC', 'usage', 'quota']
    print_user_fields = models.print_fields(exclude, 'User')
    user_lists = []
    # user_role_list = []                 #用户的角色列表
    user_role_obj = auth_models.User_Role_VDC.objects.all()
    for i in user_role_obj:
        if i.role_id != 6:
            user_id = i.user_id
            user_obj = auth_models.User.objects.get(id=user_id)
            user_lists.append(user_obj)
            # user_role_name = auth_models.Role.objects.get(id=i.role_id).name
            # user_role_list.append(user_role_name)
    return render(request, 'system_module/sys_manage_user.html', {
        'user_fields': print_user_fields,
        'user_lists': user_lists,
        # 'user_role_lists':user_role_list,
    })

def create_user(request):
    models.create_user_operation(request)
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
    auth_models.User.objects.filter(id=user_id).update(name=name,email=email)

def change_user_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    user_id = request.POST.get('user_id')
    obj = auth_models.User.objects.get(id=user_id)
    if check_password(old_password,obj.password):    #更改密码之前再次确认用户密码
        obj.password = make_password(new_password)
        obj.save()
    return HttpResponse('change passwd failed')

#------------manage Role-------------
@auth
def manage_role(request):
    exclude = ['created_time']
    print_role_fields = models.print_fields(exclude, 'Role')
    role_lists = auth_models.Role.objects.all()
    return render(request, 'system_module/sys_manage_role.html', {
        'role_fields': print_role_fields,
        'role_lists': role_lists,
    })

def create_role(request):
    name = request.POST.get('rolename')
    desc = request.POST.get('desc')
    obj = auth_models.Role(name=name,description=desc)
    obj.save()

def del_role(request):
    role_id = request.POST.get('role_id')
    if role_id > 6 :
        auth_models.User.objects.filter(id=role_id).delete()
        return redirect('/sys_manage_user')
    else:return HttpResponse('you can not delete the role')

def update_user(request):
    role_id = request.POST.get('role_id')
    if role_id > 6:
        name = request.POST.get('update_rolename')
        desc = request.POST.get('update_desc')
        auth_models.User.objects.filter(id=role_id).update(name=name, description=desc)
    else:
        return HttpResponse('you can not update the role')