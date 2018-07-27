# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import apps
from user_auth import models as auth_models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.conf import settings
# Create your models here.

def create_user_operation(request):
    name = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    department = request.POST.get('department')
    role = settings.SYSROLES['SYSUSER']
    quota_cpu = request.POST.get('cpu_amount')
    quota_ram = request.POST.get('memory')
    quota_volume = request.POST.get('volume')
    quota_instances = request.POST.get('instance_amount')
    user_obj = auth_models.User(name=name, password=make_password(password), email=email,department=department,cpu=quota_cpu,ram=quota_ram,instances=quota_instances,volume=quota_volume,recent_use_VDC=0)
    user_obj.save()
    user_role_obj = auth_models.User_Role_VDC(user_id=user_obj.id, role_id=role)
    user_role_obj.save()