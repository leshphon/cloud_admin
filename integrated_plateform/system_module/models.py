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


