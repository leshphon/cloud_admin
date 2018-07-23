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
from api.keystone import client as keystoneClient


# Create your views here.
def sys_index(request):
    return render(request, 'system_module/sys_index_overview.html')

#角色id设为全局
vdc_admin_role_id = auth_models.Role.objects.get(name='VDC_admin').id
general_user_role_id = auth_models.Role.objects.get(name='general_user').id
system_admin_role_id = auth_models.Role.objects.get(name='system_admin').id
system_maintainer_role_id = auth_models.Role.objects.get(name='system_maintainer').id
system_monitor_role_id = auth_models.Role.objects.get(name='system_monitor').id

#-----------manage VDC---------------
@auth
def manage_vdc(request):
    exclude = ['created_time', 'backend_info', 'usage']
    print_vdc_fields = models.print_fields(exclude, 'VDC')
    vdc_lists = auth_models.VDC.objects.all()
    vdc_admins_obj = auth_models.User_Role_VDC.objects.filter(role_id=vdc_admin_role_id)
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
    #管理平台创建vdc时，先通过传递quota参数在openstack后端创建对应的project 如创建成功，再在管理平台创建vdc
    quota_dict = {"cores":quota_obj.cpu,"gigabytes": quota_obj.volume, "backup_gigabytes": quota_obj.volume, "instances": quota_obj.instances, "ram": quota_obj.ram}
    cl = keystoneClient.Client()
    key = cl.attach2project(quota_params=quota_dict)
    vdc_user = cl.register_user(key=key)
    print("this is backend info",vdc_user)
    if vdc_user:
        usage = auth_models.Usage(cpu=0,ram=0,instances=0,volume=0)
        usage.save()
        vdc_obj = auth_models.VDC(name=name, description=desc, quota_id=quota_obj.id,backend_info=vdc_user,usage_id=usage.id)
        vdc_obj.save()
        request.session["backend_info"] = vdc_user
        user_vdc_obj = auth_models.User_Role_VDC(vdc_id=vdc_obj.id,user_id=vdc_admin_id,role_id=vdc_admin_role_id)
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
    exclude = ['id','password', 'created_time', 'updated_time','status', 'recent_use_VDC', 'usage', 'quota']
    print_user_fields = models.print_fields(exclude, 'User')
    user_lists = []
    # user_lists = auth_models.User.objects.all()
    # user_role_list = []                #用户的角色列表
    user_role_obj = auth_models.User_Role_VDC.objects.all()
    # for i in user_role_obj:
    #     user_role = auth_models.User_Role_VDC.objects.filter(line.id)
    #     line['role'] = user_role.role_id
    for i in user_role_obj:
        if i.role_id != general_user_role_id:
            user_dict = {}
            user_obj = i.user
            role_obj_name = i.role.name
            user_dict["user_obj"] = user_obj
            user_dict["role_name"] = role_obj_name
            user_lists.append(user_dict)
    roles = auth_models.Role.objects.all()
    return render(request, 'system_module/sys_manage_user.html', {
        'user_fields': print_user_fields,
        'user_lists': user_lists,
        'role_lists': roles,
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
    obj = auth_models.Role(name=name, description=desc)
    obj.save()

# def del_role(request):
#     role_id = request.POST.get('role_id')
#     if role_id != system_admin_role_id | vdc_admin_role_id | system_maintainer_role_id | system_monitor_role_id | general_user_role_id:
#         auth_models.User.objects.filter(id=role_id).delete()
#         return redirect('/sys_manage_user')
#     else: return HttpResponse('you can not delete the role')


def update_user(request):
    role_id = request.POST.get('role_id')
    if role_id != system_admin_role_id | vdc_admin_role_id | system_maintainer_role_id | system_monitor_role_id | general_user_role_id:
        name = request.POST.get('update_rolename')
        desc = request.POST.get('update_desc')
        auth_models.User.objects.filter(id=role_id).update(name=name, description=desc)
    else:
        return HttpResponse('you can not update the role')

def init_role(request):
    role_lists = auth_models.Role.objects.all()
    if len(role_lists):
        print("aleady inited roles")
        return redirect('/sys_manage_user')
    role1 = auth_models.Role(name='system_admin',description='this is system admin role')
    role2 = auth_models.Role(name='VDC_admin', description='this is VDC admin role')
    role3 = auth_models.Role(name='system_maintainer', description='this is system maintainer role')
    role4 = auth_models.Role(name='system_monitor', description='this is system system_monitor role')
    role5 = auth_models.Role(name='general_user', description='general_user')
    role1.save()
    role2.save()
    role3.save()
    role4.save()
    role5.save()
    right1 = auth_models.Rights(name='createUser', description='createUser')
    right2 = auth_models.Rights(name='updateUser', description='updateUser')
    right3 = auth_models.Rights(name='deleteUser', description='deleteUser')
    right4 = auth_models.Rights(name='disableUser', description='disableUser')
    right5 = auth_models.Rights(name='enableUser', description='enableUser')
    right6 = auth_models.Rights(name='createRole', description='createRole')
    right7 = auth_models.Rights(name='updateRole', description='updateRole')
    right8 = auth_models.Rights(name='deleteRole', description='deleteRole')
    right9 = auth_models.Rights(name='createVDC', description='createVDC')
    right10 = auth_models.Rights(name='updateVDC', description='updateVDC')
    right11 = auth_models.Rights(name='deleteVDC', description='deleteVDC')
    right1.save()
    right2.save()
    right3.save()
    right4.save()
    right5.save()
    right6.save()
    right7.save()
    right8.save()
    right9.save()
    right10.save()
    right11.save()
    rr1 = auth_models.Role_Rights(right_id=right1.id, role_id=role1.id)
    rr2 = auth_models.Role_Rights(right_id=right2.id, role_id=role1.id)
    rr3 = auth_models.Role_Rights(right_id=right3.id, role_id=role1.id)
    rr4 = auth_models.Role_Rights(right_id=right4.id, role_id=role1.id)
    rr5 = auth_models.Role_Rights(right_id=right5.id, role_id=role1.id)
    rr6 = auth_models.Role_Rights(right_id=right9.id, role_id=role1.id)
    rr7 = auth_models.Role_Rights(right_id=right10.id, role_id=role1.id)
    rr8 = auth_models.Role_Rights(right_id=right11.id, role_id=role1.id)
    rr1.save()
    rr2.save()
    rr3.save()
    rr4.save()
    rr5.save()
    rr6.save()
    rr7.save()
    rr8.save()
    rr9 = auth_models.Role_Rights(right_id=right1.id, role_id=role2.id)
    rr10 = auth_models.Role_Rights(right_id=right2.id, role_id=role2.id)
    rr11 = auth_models.Role_Rights(right_id=right3.id, role_id=role2.id)
    rr12 = auth_models.Role_Rights(right_id=right4.id, role_id=role2.id)
    rr13 = auth_models.Role_Rights(right_id=right5.id, role_id=role2.id)
    rr9.save()
    rr10.save()
    rr11.save()
    rr12.save()
    rr13.save()

    return redirect('/sys_manage_user')