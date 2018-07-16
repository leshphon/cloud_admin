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


# Create your views here.
def sys_index(request):
    return render(request, 'system_module/sys_index_overview.html')


@auth
def manage_vdc(request):
    exclude = ['created_time', 'backend_info', 'usage']
    vdc_obj = apps.get_model('user_auth', 'VDC')
    vdc_fields = vdc_obj._meta.fields
    print_vdc_fields = [f for f in vdc_fields if f.name not in exclude]
    vdc_lists = auth_models.VDC.objects.all()
    vdc_admins_id = auth_models.User_Role_VDC.objects.filter(role_id=3)
    vdc_admins = []
    for index in vdc_admins_id:
        vdc_admins.append(auth_models.User.objects.get(id=index.user_id))
    return render(request, 'system_module/sys_manage_vdc.html', {
        'vdc_fields': print_vdc_fields,
        'vdc_lists': vdc_lists,
        'vdc_admins': vdc_admins,
    })


@auth
def manage_user(request):
    exclude = ['password', 'created_time', 'status', 'recent_use_VDC', 'usage', 'quota']
    user_obj = apps.get_model('user_auth', 'User')
    user_fields = user_obj._meta.fields
    print_user_fields = [f for f in user_fields if f.name not in exclude]
    user_lists = auth_models.User.objects.all()
    return render(request, 'system_module/sys_manage_user.html', {
        'user_fields': print_user_fields,
        'user_lists': user_lists,
    })


@auth
def manage_role(request):
    exclude = ['created_time']
    role_obj = apps.get_model('user_auth', 'Role')
    role_fields = role_obj._meta.fields
    print_role_field = [f for f in role_fields if f.name not in exclude]
    role_lists = auth_models.Role.objects.all()
    return render(request, 'system_module/sys_manage_role.html', {
        'role_fields': print_role_field,
        'role_lists': role_lists,
    })


def create_user(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    role = request.POST.get('user_role')
    create_user_operation(name, password, email, role)
    # 返回的是user_role_vdc里的一个对象
    return redirect('/sys_manage_user')


def create_user_operation(name, password, email, role):
    user_obj = auth_models.User(name=name, password=make_password(password), email=email)
    user_obj.save()
    # print('the id is..........',user_obj.id)
    user_role_obj = auth_models.User_Role_VDC(user_id=user_obj.id, role_id=role)
    user_role_obj.save()
    print 'user_created'


def create_vdc_admin(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    role = request.POST.get('user_role')
    print(name, password, email, role)
    create_user_operation(name, password, email, role)
    return HttpResponse(serializers.serialize('json', [auth_models.User.objects.get(name=name)]))
    # return HttpResponse('ok')


def create_vdc(request):
    name = request.POST.get('vdc_name')
    desc = request.POST.get('vdc_desc')
    vdc_admin_id = request.POST.get('vdc_admin_id')
    quota_cpu = request.POST.get('cpu_amount')
    quota_ram = request.POST.get('memory')
    quota_disk = request.POST.get('disk')
    print(name, desc, vdc_admin_id, quota_cpu, quota_ram, quota_disk)
    quota_obj = auth_models.Quota(cpu=quota_cpu, ram=quota_ram, disk=quota_disk)
    quota_obj.save()
    vdc_obj = auth_models.VDC(name=name, description=desc, quota_id=quota_obj.id)
    vdc_obj.save()
    # user_role_obj = create_user('test7', 'art319', 'VDC_admin')
    # print('this is user obj::', user_role_obj)
    # print('this is user.id::', user_role_obj.id)
    # 通过update更改user_role_vdc里的对象的vdc_id
    # auth_models.User_Role_VDC.objects.filter(id=user_role_obj.id).update(vdc_id=vdc_obj.id)
    return redirect('/sys_manage_vdc')


def del_user(request):
    user_id = request.POST.get('user_id')
    print(user_id)
    auth_models.User.objects.filter(id=user_id).delete()
    return redirect('/sys_manage_user')


def get_quota(request):
    quota_id = request.POST.get('quota_id')
    print(quota_id)
    quota_detail = auth_models.Quota.objects.get(id__exact=quota_id)
    return HttpResponse(serializers.serialize('json', [quota_detail]), content_type="application/json")
