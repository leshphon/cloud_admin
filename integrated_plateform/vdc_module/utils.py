# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import apps
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
import json

from user_auth import models as auth_models
import models as vdc_models
import api.keystone.client as ksclient
import api.nova.client as nvclient


def print_fields(exclude, table_name):
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


def sync_database_all():
    print("sync at starting")
    vdc_obj = auth_models.VDC.objects.all()
    for i in range(len(vdc_obj)):
        if not vdc_obj[i].backend_info:
            continue
        print(vdc_obj[i].backend_info)
        opensatck_user = ksclient.Client().register_user(key=str(vdc_obj[i].backend_info))
        instance_json = nvclient.Client().show_servers(user=opensatck_user)
        instance_dict = json.loads(instance_json)
        if instance_dict["detect"]["code"] == 1:
            vdc_models.Server.objects.filter(created_in=vdc_obj[i].id).delete()
            for j in range(len(instance_dict["servers"])):
                temp_dict = instance_dict["servers"][j]
                vdc_models.ServerAddresses.objects.filter(server_id=temp_dict["id"]).delete()
                vdc_models.ServerVolume.objects.filter(server_id=temp_dict["id"]).delete()
                vdc_models.ServerSecurityGroup.objects.filter(server_id=temp_dict["id"]).delete()
                if temp_dict.get("os-extended-volumes:volumes_attached"):
                    volume_dict = temp_dict["os-extended-volumes:volumes_attached"]
                    volume_num = len(volume_dict)
                    for k in range(volume_num):
                        instance_volume_obj = vdc_models.ServerVolume(server_id=temp_dict["id"],
                                                                      volume_id=
                                                                      volume_dict[k]["id"])
                        instance_volume_obj.save()
                if temp_dict.get("addresses"):
                    for key in temp_dict["addresses"].keys():
                        addr_dict = temp_dict["addresses"][key]
                        addr_num = len(addr_dict)
                        for k in range(addr_num):
                            instance_addr_obj = vdc_models.ServerAddresses(server_id=temp_dict["id"],
                                                                           net_name=key,
                                                                           net_addr=addr_dict[k]["addr"],
                                                                           net_type=addr_dict[k]["OS-EXT-IPS:type"],
                                                                           net_mac_addr=addr_dict[k][
                                                                               "OS-EXT-IPS-MAC:mac_addr"]
                                                                           )
                            instance_addr_obj.save()
                if temp_dict.get("security_groups"):
                    security_groups_num = len(temp_dict["security_groups"])
                    # delete same items
                    no_same_security_groups = []
                    for sg in temp_dict["security_groups"]:
                        if sg not in no_same_security_groups:
                            no_same_security_groups.append(sg)
                    for k in range(security_groups_num):
                        instance_sg_obj = vdc_models.ServerSecurityGroup(server_id=temp_dict["id"],
                                                                         security_group_name=
                                                                         temp_dict["security_groups"][k]["name"])
                        instance_sg_obj.save()
                if not temp_dict["image"]:
                    image_params = ""
                else:
                    image_params = temp_dict["image"]["id"]
                if not temp_dict["metadata"].get("owner"):
                    owner_params = ""
                else:
                    owner_params = temp_dict["metadata"]["owner"]
                instance_obj = vdc_models.Server(name=temp_dict["name"],
                                                 identification=temp_dict["id"],
                                                 created_by=owner_params,  # user_id
                                                 created_in=vdc_obj[i].id,  # project_id
                                                 flavor_id=temp_dict["flavor"]["id"],
                                                 image_id=image_params,
                                                 host_id=temp_dict["hostId"],
                                                 status=temp_dict["status"],
                                                 task_state=temp_dict["OS-EXT-STS:task_state"],
                                                 vm_state=temp_dict["OS-EXT-STS:vm_state"],
                                                 created_time=temp_dict["created"],
                                                 updated_time=temp_dict["updated"],
                                                 key_name=temp_dict["key_name"],
                                                 )
                instance_obj.save()
        else:
            print("sync error!")
        ksclient.Client().revoke_user(opensatck_user)


def sync_database_single(user, server_id):
    print("sync at modifying instance")
    modify_num = len(server_id)

    # vdc_obj = auth_models.VDC.objects.filter(id=)
    for i in range(modify_num):
        instance_json = nvclient.Client().show_servers(user=user, identification=server_id[i])
        instance_dict = json.loads(instance_json)
        if instance_dict["detect"]["code"] == 1:
            # vdc_models.Server.objects.filter(created_by=).update()
            for j in range(len(instance_dict["servers"])):
                temp_dict = instance_dict["servers"][j]
                vdc_models.ServerAddresses.objects.filter(server_id=temp_dict["id"]).delete()
                vdc_models.ServerVolume.objects.filter(server_id=temp_dict["id"]).delete()
                vdc_models.ServerSecurityGroup.objects.filter(server_id=temp_dict["id"]).delete()
                if temp_dict.get("os-extended-volumes:volumes_attached"):
                    volume_dict = temp_dict["os-extended-volumes:volumes_attached"]
                    volume_num = len(volume_dict)
                    for k in range(volume_num):
                        instance_volume_obj = vdc_models.ServerVolume(server_id=temp_dict["id"],
                                                                      volume_id=
                                                                      volume_dict[k]["id"])
                        instance_volume_obj.save()
                if temp_dict.get("addresses"):
                    for key in temp_dict["addresses"].keys():
                        addr_dict = temp_dict["addresses"][key]
                        addr_num = len(addr_dict)
                        for k in range(addr_num):
                            instance_addr_obj = vdc_models.ServerAddresses(server_id=temp_dict["id"],
                                                                           net_name=key,
                                                                           net_addr=addr_dict[k]["addr"],
                                                                           net_type=addr_dict[k]["OS-EXT-IPS:type"],
                                                                           net_mac_addr=addr_dict[k][
                                                                               "OS-EXT-IPS-MAC:mac_addr"]
                                                                           )
                            instance_addr_obj.save()
                if temp_dict.get("security_groups"):
                    security_groups_num = len(temp_dict["security_groups"])
                    # delete same items
                    no_same_security_groups = []
                    for sg in temp_dict["security_groups"]:
                        if sg not in no_same_security_groups:
                            no_same_security_groups.append(sg)
                    for k in range(security_groups_num):
                        instance_sg_obj = vdc_models.ServerSecurityGroup(server_id=temp_dict["id"],
                                                                         security_group_name=
                                                                         temp_dict["security_groups"][k]["name"])
                        instance_sg_obj.save()
                if not temp_dict["image"]:
                    image_params = ""
                else:
                    image_params = temp_dict["image"]["id"]
                if not temp_dict["metadata"].get("owner"):
                    owner_params = ""
                else:
                    owner_params = temp_dict["metadata"]["owner"]
                instance_obj = vdc_models.Server(name=temp_dict["name"],
                                                 identification=temp_dict["id"],
                                                 created_by=owner_params,  # user_id
                                                 created_in=vdc_obj[i].id,  # project_id
                                                 flavor_id=temp_dict["flavor"]["id"],
                                                 image_id=image_params,
                                                 host_id=temp_dict["hostId"],
                                                 status=temp_dict["status"],
                                                 task_state=temp_dict["OS-EXT-STS:task_state"],
                                                 vm_state=temp_dict["OS-EXT-STS:vm_state"],
                                                 created_time=temp_dict["created"],
                                                 updated_time=temp_dict["updated"],
                                                 key_name=temp_dict["key_name"],
                                                 )
                instance_obj.save()
        else:
            print("sync error!")
        ksclient.Client().revoke_user(opensatck_user)
# def instance_status():
#
#     status = {
#
#     None:""
#     BUDILDING
#     IMAGE_SNAPSHOTTING
#     IMAGE_BACKINGUP
#     UPDATING_PASSWORD
#     PAUSING
#     UNPAUSING
#     SUSPENDING
#     RESUMING
#     DELETING
#     STOPPING
#     STARTING
#     RESCUING
#     UNRESCUING
#     REBOOTING
#     REBUILDING
#     POWERING_ON
#     POWERING_OFF
#     RESIZING
#     RESIZE_REVERTING
#     RESIZE_CONFIRMING
#     SCHEDULING
#     BLOCK_DEVICE_MAPPING
#     NETWORKING
#     SPAWNING
#     RESIZE_PREP
#     RESIZE_MIGRATING
#     RESIZE_MIGRATED
#     RESIZE_FINISH
#
#     }
