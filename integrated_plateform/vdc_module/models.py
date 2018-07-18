# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import apps
from user_auth import models as auth_models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
# Create your models here.
def print_fields(exclude,table_name):
    obj = apps.get_model('user_auth',table_name)
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