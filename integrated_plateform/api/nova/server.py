# coding=utf-8
import json
import requests

import utils


# def struc_server(result):
#     if not result["image"]:
#         return Server(name=result["name"], identification=result["id"], created=result["created"],
#                       updated=result["updated"], flavor_id=result["flavor"]["id"], image="", key_name=["key_name"],
#                       owner=result["metadata"]["owner"], security_groups=result["security_groups"],
#                       status=result["status"], task_state=result["OS-EXT-STS:task_state"],
#                       vm_state=result["OS-EXT-STS:vm_state"], volume=result["os-extended-volumes:volumes_attached"],
#                       addresses=result["addresses"], hostId=result["hostId"])
#     return Server(name=result["name"], identification=result["id"], created=result["created"],
#                   updated=result["updated"],
#                   flavor_id=result["flavor"]["id"], image=result["image"]["id"], key_name=["key_name"],
#                   owner=result["metadata"]["owner"], security_groups=result["security_groups"],
#                   status=result["status"], task_state=result["OS-EXT-STS:task_state"],
#                   vm_state=result["OS-EXT-STS:vm_state"], volume=result["os-extended-volumes:volumes_attached"],
#                   addresses=result["addresses"], hostId=result["hostId"])


class ServerManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, owner=None, identification=None):
        list_result = []
        url = self.user.endpoint['nova'] + '/servers'
        # TODO(dc): system user access nova
        # if self.user.flag == 'sys':
        #     result = requests.get(self.user.endpoint['nova'], data=None,
        #                           headers=self.user.headers).json()
        #     for i in range(len(result["servers"])):
        #         dict_result.append(self.struc_server(result["servers"]))
        #     return dict_result
        if identification is not None:
            result = requests.get(url=url + '/detail' + '?uuid=' + identification, data=None, headers=self.user.headers)
            # if utils.answer_detect(result, flag='dict')['detect']['code'] == 1:
            #     return list_result.append(struc_server(result.json()["servers"][0]))
            # else:
            #     return utils.answer_detect(result)
            return utils.answer_detect(result)
        result = requests.get(url=url + '/detail', data=None, headers=self.user.headers)
        # if utils.answer_detect(result, flag='dict')['detect']['code'] == 1:
        #     result_dict = result.json()
        #     result_len = len(result_dict["servers"])
        #     for i in range(result_len):
        #         if not result_dict["servers"][i]["metadata"]:
        #             continue
        #         if owner is None:
        #             list_result.append(struc_server(result_dict["servers"][i]))
        #         elif owner == result_dict["servers"][i]["metadata"]["owner"]:
        #             list_result.append(struc_server(result_dict["servers"][i]))
        #     return list_result
        # else:
        #     return utils.answer_detect(result)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        url = self.user.endpoint['nova'] + '/servers'
        params = {
            "server": {
                "networks": [],
                "metadata": {}
            }
        }
        params["server"]["name"] = kwargs["name"]
        params["server"]["flavorRef"] = kwargs["flavorRef"]
        if kwargs.get("net_uuid") is not None:
            params["server"]["networks"].append({"uuid": kwargs["net_uuid"]})
        if kwargs.get("port_id") is not None:
            params["server"]["networks"].append({"port": kwargs["port_id"]})
        # blank,image,snapshot,volume and image,snapshot,volume need <destination_type> is volume
        if kwargs.get("source_type"):
            params["server"]["block_device_mapping_v2"] = [
                {
                    "boot_index": 0,
                    "source_type": kwargs["source_type"]
                }
            ]
        # local or volume
        if kwargs.get("destination_type"):
            params["server"]["block_device_mapping_v2"][0]["destination_type"] = kwargs["destination_type"]
        if kwargs.get("source_uuid") is not None:
            params["server"]["block_device_mapping_v2"][0]["uuid"] = kwargs["source_uuid"]
        if kwargs.get("delete_on_termination") is not None:
            params["server"]["block_device_mapping_v2"][0]["delete_on_termination"] = kwargs["delete_on_termination"]
        if kwargs.get("volume_size") is not None:
            params["server"]["block_device_mapping_v2"][0]["volume_size"] = kwargs["volume_size"]
        if kwargs.get("destination_type") is not None:
            params["server"]["block_device_mapping_v2"][0]["destination_type"] = kwargs["destination_type"]
        if kwargs.get("imageRef") is not None:
            params["server"]["imageRef"] = kwargs["imageRef"]
            mode = 'local'

        if kwargs.get("OS-DCF:diskConfig"):
            params["server"]["OS-DCF:diskConfig"] = kwargs["OS-DCF:diskConfig"]
        if kwargs.get("security_groups"):
            params["server"]["security_groups"] = kwargs["security_groups"]
        if kwargs.get("tags"):
            params["server"]["tags"] = [kwargs["tags"]]
        if kwargs.get("owner"):
            params["server"]["metadata"]["owner"] = kwargs["owner"]

        result = requests.post(url=url, data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        list_result = []
        url = self.user.endpoint['nova'] + '/servers'
        params = {
            "server": {
            }
        }
        if kwargs.get("name") is not None:
            params["server"]["name"] = kwargs["name"]
        if kwargs.get("OS-DCF:diskConfig") is not None:
            params["server"]["OS-DCF:diskConfig"] = kwargs["OS-DCF:diskConfig"]
        result = requests.put(url=url + '/' + identification, data=json.dumps(params),
                              headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        url = self.user.endpoint['nova'] + '/servers'
        result = requests.delete(url=url + '/' + identification, headers=self.user.headers)
        return utils.answer_detect(result)

    def manipulate_without_params(self, action, identification):
        url = self.user.endpoint['nova'] + '/servers/' + identification + '/action'
        action_set = {
            "start": {"os-start": None},
            "stop": {"os-stop": None},
            "pause": {"pause": None},
            "unpause": {"unpause": None},
            "suspend": {"suspend": None},
            "unsuspend": {"unsuspend": None},
            "lock": {"lock": None},
            "unlock": {"unlock": None},
            "shelve": {"shelve": None},
            "unshelve": {"unshelve": None},
            "shelveOffload": {"shelveOffload": None},
            "hard_reboot": {"reboot": {"type": "HARD"}},
            "soft_reboot": {"reboot": {"type": "SOFT"}},
            "revert_resize": {"revertResize": None},
            "confirm_resize": {"confirmResize": None},
            "unrescue": {"unrescue": None}
        }
        result = requests.post(url=url, data=json.dumps(action_set[action]), headers=self.user.headers)
        return utils.answer_detect(result)

    def manipulate_with_params(self, action, identification, **kwargs):
        url = self.user.endpoint['nova'] + '/servers/' + identification + '/action'
        action_set = {"snapshot": {"createImage": {}},
                      "live_migrate": {"os-migrateLive": {"block_migration": "auto", "force": False}},
                      "rebuild": {"rebuild": {}},
                      "rescue": {"rescue": {}},
                      "resize": {"resize": {}},
                      }
        if action == "snapshot":
            action_set[action]["createImage"]["name"] = kwargs["name"]
        if action == "livemigrate":
            action_set[action]["livemigrate"]["migrateLive"]["host"] = kwargs["host_id"]
        if action == "rebuild":
            action_set[action]["rebuild"]["imageRef"] = kwargs[""]
            if kwargs.get("name"):
                action_set[action]["rebuild"]["name"] = kwargs["name"]
            if kwargs.get("key_name"):
                action_set[action]["rebuild"]["key_name"] = kwargs["key_name"]
        if action == "rescue":
            if kwargs.get("imageRef"):
                action_set[action]["rescue"]["rescue_image_ref"] = kwargs["imageRef"]
        if action == "resize":
            action_set[action]["resize"]["flavorRef"] = kwargs["flavorRef"]
        result = requests.post(url=url, data=json.dumps(action_set[action]), headers=self.user.headers)
        return utils.answer_detect(result)

#
# class Server(object):
#     def __init__(self, name, identification, created, updated,
#                  flavor_id, image, key_name, owner,
#                  security_groups, status, task_state, vm_state,
#                  volume, addresses, hostId):
#         self.name = name
#         self.identification = identification
#         self.created = created
#         self.updated = updated
#         self.addresses = addresses
#         self.flavor_id = flavor_id
#         self.flavor_obj = None
#         self.image = image
#         self.key_name = key_name
#         self.owner = owner
#         self.security_groups = security_groups
#         self.status = status
#         self.task_state = task_state
#         self.vm_state = vm_state
#         self.volume = volume
#         self.hostId = hostId
