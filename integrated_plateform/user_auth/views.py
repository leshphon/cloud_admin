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
from api.keystone import client as keystoneClient
from django.conf import settings

# Create your views here.

host = "10.190.2.226"
user = "root"
passwd = "art319"
db = "PPIDB"
port = 3306
charset = "utf8"

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

                    # 判断用户角色并进入相应页面
                    login_rel_objs = models.User_Role_VDC.objects.filter(user_id=login_obj.id)

                    cl = keystoneClient.Client()

                    # log_rel_objs是login用户的所有角色、vdc信息
                    if login_rel_objs.__len__() == 1 and login_rel_objs.first().role_id == settings.SYSROLES['SYSADMIN']:       # 系统用户没有VDC关系,因此一个系统用户只有一条记录
                        system_user = cl.register_user(auth='system')
                        request.session["openstack_user"] = system_user
                        request.session['login_role'] = login_rel_objs.first().role_id
                        return render(request, 'system_module/sys_index_overview.html')
                    else:
                        if login_obj.recent_use_VDC == 0:
                            VDC_id = login_rel_objs.first().vdc_id      # 将第一个关系中的vdc_id赋给recent_user_vdc
                            login_obj.recent_use_VDC = VDC_id           # 更新数据库
                            login_obj.save()
                        recent_use_VDC_id = login_obj.recent_use_VDC
                        login_rel_obj = models.User_Role_VDC.objects.filter(user_id=login_obj.id,vdc_id=recent_use_VDC_id)
                        request.session['login_role'] = login_rel_obj.first().role_id
                        request.session['login_user_recent_vdc'] = recent_use_VDC_id    #将recent_use_vdc也存入session中
                        if login_rel_obj.first().role_id == settings.SYSROLES['SYSVDC']:
                            vdc_obj = login_rel_obj.first().vdc
                            vdc_user = cl.register_user(key=str(vdc_obj.backend_info))
                            request.session["openstack_user"] = vdc_user
                            print("this is backend info", request.session.get("openstack_user"))
                            return render(request, 'vdc_module/vdc_index.html')
                        elif login_rel_obj.role_id == settings.SYSROLES['SYSUSER']:
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

def login2(request):
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

                    # 判断用户角色并进入相应页面
                    login_rel_objs = models.User_Role_VDC.objects.filter(user_id=login_obj.id)

                    cl = keystoneClient.Client()

                    # log_rel_objs是login用户的所有角色、vdc信息
                    if login_rel_objs.__len__() == 1 and login_rel_objs.first().role_id == settings.SYSROLES['SYSADMIN']:       # 系统用户没有VDC关系,因此一个系统用户只有一条记录
                        system_user = cl.register_user(auth='system')
                        request.session["openstack_user"] = system_user
                        request.session['login_role'] = login_rel_objs.first().role_id
                        return render(request, 'system_module/sys_index_overview.html')
                    else:
                        if login_obj.recent_use_VDC == 0:
                            VDC_id = login_rel_objs.first().vdc_id      # 将第一个关系中的vdc_id赋给recent_user_vdc
                            login_obj.recent_use_VDC = VDC_id           # 更新数据库
                            login_obj.save()
                        recent_use_VDC_id = login_obj.recent_use_VDC
                        login_rel_obj = models.User_Role_VDC.objects.filter(user_id=login_obj.id,vdc_id=recent_use_VDC_id)
                        request.session['login_role'] = login_rel_obj.first().role_id
                        request.session['login_user_recent_vdc'] = recent_use_VDC_id    #将recent_use_vdc也存入session中
                        if login_rel_obj.first().role_id == settings.SYSROLES['SYSVDC']:
                            vdc_obj = login_rel_obj.first().vdc
                            vdc_user = cl.register_user(key=str(vdc_obj.backend_info))
                            request.session["openstack_user"] = vdc_user
                            print("this is backend info", request.session.get("openstack_user"))
                            return render(request, 'vdc_module/vdc_index.html')
                        elif login_rel_obj.role_id == settings.SYSROLES['SYSUSER']:
                            return HttpResponse('这是一个普通用户，页面还在制作')
                else:
                    error = '密码错误'
                    return render(request, 'user_auth/login2.html', {
                        'error': error,
                    })
        except:
            error = 'user does not exist'
            return render(request, 'user_auth/login2.html', {
                'error': error,
            })
    return render(request, 'user_auth/login2.html')

def logout(request):
    try:
        del request.session['username']
        del request.session['password']
        return render(request, 'user_auth/login.html')
    except:
        return render(request, 'user_auth/login.html')





