# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from user_auth import models as auth_models
from django.db import models
from django.apps import apps
from django.forms import models,fields
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from api.keystone import client

# Create your models here.

def print_fields(exclude,table_name):
    obj = apps.get_model('user_auth', table_name)
    obj_fields = obj._meta.fields
    print_fields_list = [f for f in obj_fields if f.name not in exclude]
    return print_fields_list


def create_user_operation(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    role = request.POST.get('user_role')
    user_obj = auth_models.User(name=name, password=make_password(password), email=email)
    user_obj.save()
    user_role_obj = auth_models.User_Role_VDC(user_id=user_obj.id, role_id=role)
    user_role_obj.save()
    print 'user_created'


def quota_create(request):
    quota_cpu = request.POST.get('cpu_amount')
    print("iiiiiiiiiiiiiiiiiiii:",quota_cpu)
    quota_ram = request.POST.get('memory')
    quota_volume = request.POST.get('volume')
    quota_instances = request.POST.get('instance_amount')
    quota_obj = auth_models.Quota(cpu=quota_cpu, ram=quota_ram, volume=quota_volume,instances=quota_instances)
    quota_obj.save()
    return quota_obj
