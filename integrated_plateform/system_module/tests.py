# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

from user_auth import models as auth_models
# Create your tests here.

# This will create some test data in db, please comment if data exit


def init_admin_user():
    user_lists = auth_models.User.objects.all()
    vdc_lists = auth_models.VDC.objects.all()
    if len(user_lists):
        print("already inited admin user")
    else:
        print("init an admin user")
        sys_admin_user = auth_models.User(name="admin", password=make_password("admin"), department='')
        sys_admin_user.save()
        sys_user_role = auth_models.User_Role_VDC(user_id=sys_admin_user.id, role_id=1)
        sys_user_role.save()
    if len(vdc_lists):
        print("already exist VDC not to inited test vdc")
    else:
        print("init test vdc and its admin user")
        vdc_admin_user = auth_models.User(name="vdcAdmin", password=make_password("art319"), department='')
        vdc_admin_user.save()
        key = ("DQvsrCWt8Ap_" + "11C4C=_NFpnO" + "5Y4xU[" + "\\" + "\\" + "}Ku5")
        test_vdc = auth_models.VDC(name="test_vdc", backend_info=key, description='', cpu=50, ram=600000, volume=500,
                                   instances=50)
        vdc_user_role = auth_models.User_Role_VDC(user_id=vdc_admin_user.id, role_id=2, vdc=test_vdc.id)
        vdc_user_role.save()
        test_vdc.save()
