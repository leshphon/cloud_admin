from django.db import models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)


class User(models.Model):
    name = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=64, blank=True)
    password = models.CharField(max_length=128)
    status = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)
    updated_time = models.DateField(auto_now=True)
    recent_use_VDC = models.IntegerField(default=0, blank=True)
    department = models.CharField(max_length=32, null=True)
    cpu = models.IntegerField(default=None)
    ram = models.IntegerField(default=None)
    volume = models.IntegerField(default=None)
    instances = models.IntegerField(default=None)
    used_cpu = models.IntegerField(default=None)
    used_ram = models.IntegerField(default=None)
    used_volume = models.IntegerField(default=None)
    used_instances = models.IntegerField(default=None)


class Role(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(max_length=500, default=None)
    created_time = models.DateField(auto_now_add=True)
    updated_time = models.DateField(auto_now=True)


#
class VDC(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(default=None)
    created_time = models.DateField(auto_now_add=True)
    updated_time = models.DateField(auto_now=True)
    backend_info = models.TextField(default=None)
    cpu = models.IntegerField(default=None)
    ram = models.IntegerField(default=None)
    volume = models.IntegerField(default=None)
    instances = models.IntegerField(default=None)
    used_cpu = models.IntegerField(default=None)
    used_ram = models.IntegerField(default=None)
    used_volume = models.IntegerField(default=None)
    used_instances = models.IntegerField(default=None)


#
class Rights(models.Model):
    name = models.CharField(max_length=32,unique=True)
    description = models.TextField(blank=True)
#


class User_Role_VDC(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE,null=True)
    vdc = models.ForeignKey('VDC', on_delete=models.CASCADE,null=True)

    # class Meta:
    #     unique_together = ("user","role","vdc")


class Role_Rights(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    right = models.ForeignKey('Rights', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "right")


