#coding=utf-8
from django.shortcuts import render_to_response,render,redirect
from django.http import HttpResponse
import MySQLdb
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.core import serializers
# import user_auth.model.identity as identity
import json
from . import models
import os


# Create your views here.

host = "10.190.2.226"
user = "root"
passwd = "art319"
db = "PPIDB"
port = 3306
charset = "utf8"


# def auth(func):
#     def inner(request, *args, **kwargs):
#         ck = request.session.get("username")
#         # '''如果没有登陆返回到login.html'''
#         if not ck:
#             return render(request, 'user_auth/login.html')
#         return func(request, *args, **kwargs)
#     return inner


def auth(func):
    print("come auth")

    def inner(request, *args, **kwargs):
        print('come inner')
        ck = request.session.get("username")
        print('this is ck:', ck)
        # '''如果没有登陆返回到login.html'''
        if not ck:
            return render(request, 'user_auth/login.html')
        # 判断用户权限
        role_id = request.session.get("login_role")
        print('this is role_id from session',role_id)
        rights = models.Role_Rights.objects.filter(role_id=role_id)
        print('123345:',rights)
        return func(request, *args, **kwargs)
    return inner


def login(request):
    if request.method == 'POST':
        name = request.POST.get('Username')
        password = request.POST.get('Password')
        try:
            login_obj = models.User.objects.get(name__exact=name)
            if login_obj:
                if check_password(password, login_obj.password):
                    request.session['username'] = name
                    request.session['password'] = password
                    request.session.set_expiry(60 * 15)
                    print('this is session.username', request.session.get("username"))
                    # 判断用户角色并进入相应页面
                    login_rel_objs = models.User_Role_VDC.objects.filter(user_id=login_obj.id)      # log_rel_objs是login用户的所有角色、vdc信息
                    if login_rel_objs.__len__() == 1 and login_rel_objs.first().role_id == 1:       # 系统用户没有VDC关系,因此一个系统用户只有一条记录
                        request.session['login_role'] = login_rel_objs.first().role_id
                        print('save role_id in session', request.session.get("login_role"))
                        return render(request, 'system_module/sys_index_overview.html')
                    else:
                        if login_obj.recent_use_VDC == 0:
                            VDC_id = login_rel_objs.first().vdc_id      # 将第一个关系中的vdc_id赋给recent_user_vdc
                            login_obj.recent_use_VDC = VDC_id           # 更新数据库
                            login_obj.save()
                        recent_use_VDC_id = login_obj.recent_use_VDC
                        login_rel_obj = models.User_Role_VDC.objects.get(user_id=login_obj.id, vdc_id=recent_use_VDC_id)
                        request.session['login_role'] = login_rel_obj.role_id
                        print('save role_id in session',request.session.get("login_role"))
                        if login_rel_obj.role_id == 3:
                            print('success!!!')
                            return render(request, 'vdc_module/vdc_index.html')
                        elif login_rel_obj.role_id == 6:
                            return HttpResponse('这是一个普通用户，页面还在制作')
                else:
                    error = '密码错误'
                    return render(request, 'user_auth/login.html', {
                        'error': error,
                    })
        except:
            error = 'user does not exist'
            return render(request, 'user_auth/login.html', {
                'error': error,
            })
    return render(request, 'user_auth/login.html')


# def login(request):
#     if request.method == 'POST':
#         name = request.POST.get('Username')
#         password = request.POST.get('Password')
#         try:
#             login_obj = models.User.objects.get(name__exact=name)
#             if login_obj:
#                 print(login_obj.name)
#                 if check_password(password, login_obj.password):
#                     print('password check ok')
#                     request.session['username'] = name
#                     request.session['password'] = password
#                     request.session.set_expiry(60 * 15)
#                     # 判断用户角色并进入相应页面
#                     log_user_id = login_obj.id
#                     print(log_user_id)
#                     # 返回第一个role_id。之后可以切换vdc
#                     log_user_role_id = models.User_Role_VDC.objects.filter(user_id=log_user_id).first().role_id
#                     print(log_user_role_id)
#                     log_user_role = models.Role.objects.get(id=log_user_role_id).name
#                     if log_user_role == 'system_admin':
#                         return render(request, 'system_module/sys_index_overview.html')
#                     elif log_user_role == 'VDC_admin':
#                         return render(request, 'vdc_module/vdc_index.html')
#                     else:
#                         res = models.User.objects.get(id=log_user_id)
#                         # return redirect('/vdc_instance_manage/')
#                         return HttpResponse('这是一个普通用户，页面还在制作')
#                 else:
#                     error = '密码错误'
#                     return render(request, 'user_auth/login.html', {
#                         'error': error,
#                     })
#         except:
#             error = 'user does not exist'
#             return render(request, 'user_auth/login.html', {
#                 'error': error,
#             })
#     return render(request, 'user_auth/login.html')


# def login(request):
#     if request.method == 'POST':
#         name = request.POST.get('Username')
#         password = request.POST.get('Password')
#         try:
#             obj = models.User.objects.get(name__exact=name)
#             if obj:
#                 # print(obj.name)
#                 if check_password(password, obj.password):
#                     request.session['username'] = name
#                     request.session['password'] = password
#                     request.session.set_expiry(60 * 30)
#                     # 判断用户角色并进入相应页面
#                     log_user_id = models.User.objects.get(name=name).id
#                     # print("this is thr log_user_id:", str(log_user_id))
#                     log_user_role_id = models.User_Role.objects.get(user_id=log_user_id).role_id
#                     # print("this is thr log_user_role_id:", log_user_role_id)
#                     log_user_role = models.Role.objects.get(id=log_user_role_id).name
#                     # print("this is the log_user_role:",log_user_role)
#                     if log_user_role == 'system_admin':
#                         return render(request, 'system_module/sys_index_overview.html')
#                     elif log_user_role == 'VDC_admin':
#                         return render(request, 'vdc_module/vdc_index.html')
#                     else:
#                         res = models.User.objects.get(id=log_user_id)
#                         # return redirect('/vdc_instance_manage/')
#                         return HttpResponse('这是一个普通用户，页面还在制作')
#                 else:
#                     error = '密码错误'
#                     return render(request, 'user_auth/login.html', {
#                         'error': error,
#                     })
#         except:
#             error = 'user does not exist'
#             return render(request, 'user_auth/login.html', {
#                 'error': error,
#             })
#     return render(request, 'user_auth/login.html')


def logout(request):
    try:
        del request.session['username']
        del request.session['password']
        return render(request, 'user_auth/login.html')
    except:
        return render(request, 'user_auth/login.html')


# @auth
# def index(request):
#     return render(request, 'main_base.html')


def user_create(name, password, role):
    # role::system_admin\VDC_admin\general_user\system_maintainer\system_monitor
    user_obj = models.User(name=name, password=make_password(password))
    user_obj.save()
    role_id = models.Role.objects.get(name=role).id
    # print('the id is..........',user_obj.id)
    user_role_obj = models.User_Role_VDC(user_id=user_obj.id, role_id=role_id)
    user_role_obj.save()
    return user_obj
# user_create('test..','art319','VDC_admin')


def vdc_create():
    name = 'vdc4'
    desc = 'test'
    quota_cpu = '2'
    quota_ram = '128'
    quota_disk = '256'
    quota_obj = models.Quota(cpu=quota_cpu, ram=quota_ram, disk=quota_disk)
    quota_obj.save()
    vdc_obj = models.VDC(name=name, description=desc, quota_id=quota_obj.id)
    vdc_obj.save()
    user_obj = user_create('test7', 'art319', 'VDC_admin')
    print('this is user obj::', user_obj)
    print('this is user.id::', user_obj.id)
    user_vdc_obj = models.User_VDC(user_id=user_obj.id, vdc_id=vdc_obj.id)
    user_vdc_obj.save()
# vdc_create()






#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
def user_create(name, password):
    obj = models.User(name=name, password=make_password(password))
    obj.save()
# user_create('test5','art319')
def role_create(name,desc):
    obj = models.Role(name=name, description=desc)
    obj.save()
# role_create('system_monitor','this is system monitor role')
def vdc_create(name,desc,quota_id):
    obj = models.VDC(name=name, description=desc,quota_id=quota_id)
    obj.save()
# vdc_create('vdc1','test vdc',1)
def quota_create(cpu,ram,disk):
    obj = models.Quota(cpu=cpu, ram=ram, disk=disk)
    obj.save()
# quota_create(2,128,256)
def vdc_add_user(user_id,vdc_id):
    obj = models.User_VDC(user_id=user_id, vdc_id=vdc_id)
    obj.save()
# vdc_add_user(7,1)

#需要判断如果一个用户已经加入一个角色，那不能再加
def user_add_role(user_id,role_id):
    obj = models.User_Role(user_id=user_id, role_id=role_id)
    obj.save()
# user_add_role(9,4)


# user_create('test001', 'art319')


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# def project_list(request):
#     res = identity.project_list()
#     return render(request,'identity_list.html',{"contents":res})
#
# def project_info(request):
#     data = identity.project_list()
#     res = json.dumps(data)
#     # print(res)
#     return HttpResponse(res,content_type="application/json")
#
# def group_list(request):
#     res = identity.group_list()
#     return render(request,'identity_list.html',{"contents":res})
#
# def group_list_for_member(request):
#     group_all = identity.group_list()
#     # print json.dumps(group_all)
#     # print HttpResponse(group_all)
#     # group_existed = identity.
#     return HttpResponse(json.dumps(group_all))
#
# def user_list(request):
#     res = identity.user_list()
#     return render(request,'identity_list.html',{"contents":res})
#
# def user_list_for_member(request):
#     res = identity.user_list()
#     return HttpResponse(json.dumps(res))
#
# def role_list(request):
#     res = identity.role_list()
#     return render(request,'role.html',{"contents":res})
#
# def identity_set_create(request):
#     param = request.GET.get("data")
#     print(param)
#     info = json.loads(param)
#     print(info['type'])
#     res = identity.set_create(info)
#     print(res)
#     return HttpResponse("prj创建成功")
#
# def identity_user_create(request):
#     param = request.GET.get("data")
#     print(param)
#     info = json.loads(param)
#     print(info['type'])
#     print(info['password'])
#     res = identity.user_create(info['name'],info['description'],info['password'])
#     print(res)
#     return HttpResponse("prj创建成功")
#
# def identity_delete(request):
#     param = request.GET.get("id")
#     res = identity.ide_delete(param)
#     # print(param)
#     # print(res)
#     return HttpResponse('delete successful')
#
# def set_mem_list(request, param1, param2):
#     print(param2)
#     res = identity.mem_in_set_list(param1)
#     # return HttpResponse("the param1 is :" + param1)
#     return render(request, 'member_page.html', {"contents": res,
#                                                 'identity_id': param1,
#                                                 'identity_type': param2
#                                                 })
#
# def set_add_member(request):
#     set_id = json.loads(request.GET.get("set_id"))      #int
#     mem_id_list = json.loads(request.GET.get("mem_id"))
#     print("2222222222222:",mem_id_list)#list
#     for i in range(len(mem_id_list)):
#         mem_id = mem_id_list[i]
#         print("3333333333333:",mem_id)
#         identity.set_add_member(set_id, mem_id)
#     return HttpResponse('add member successful')
#
# def set_delete_member(request):
#     set_id = json.loads(request.GET.get("set_id"))      #int
#     mem_id_list = json.loads(request.GET.get("mem_id"))
#     print("2222222222222:",mem_id_list)#list
#     for i in range(len(mem_id_list)):
#         mem_id = mem_id_list[i]
#         print("3333333333333:",mem_id)
#         identity.delete_mem_from_set(set_id, mem_id)
#     return HttpResponse('delete member successful')
#
# def ide_update(request):
#     param = request.GET.get("data")
#     print(param)
#     info = json.loads(param)
#     # print(info['id'])
#     res = identity.ide_update(info['name'],info['description'],info['id'])
#     print(res)
#     return HttpResponse("11111111111111111")


