from django.db import models
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)


class Server(models.Model):
    name = models.CharField(max_length=32)
    identification = models.CharField(max_length=128)
    created_by = models.CharField(max_length=128, null=True, blank=True)  # user_id
    created_in = models.IntegerField(default=None)  # project_id
    flavor_id = models.CharField(max_length=128)
    image_id = models.CharField(max_length=128, null=True)
    host_id = models.CharField(max_length=128)
    status = models.CharField(max_length=32)
    task_state = models.CharField(max_length=32, null=True)
    vm_state = models.CharField(max_length=32)
    created_time = models.CharField(max_length=128)
    updated_time = models.CharField(max_length=128)
    key_name = models.CharField(max_length=32, null=True)


class ServerVolume(models.Model):
    server_id = models.CharField(max_length=128)
    volume_id = models.CharField(max_length=128)


class ServerAddresses(models.Model):
    server_id = models.CharField(max_length=128)
    net_name = models.CharField(max_length=128)
    net_type = models.CharField(max_length=128)
    net_addr = models.CharField(max_length=128)
    net_mac_addr = models.CharField(max_length=128)


class ServerSecurityGroup(models.Model):
    server_id = models.CharField(max_length=128)
    security_group_name = models.CharField(max_length=128)
