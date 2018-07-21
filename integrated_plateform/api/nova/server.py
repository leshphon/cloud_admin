# coding=utf-8
import json
import requests

import utils
import flavor


def struc_server(result):
    return Server(name=result["name"], identification=result["id"], created=result["created"],
                  updated=result["updated"],
                  description=result["description"], flavor_obj=flavor.struct_flavor(result["flavor"]),
                  image=result["image"]["id"], key_name=["key_name"],  # metadata=result["metadata"],
                  security_groups=result["security_groups"]["name"], status=result["status"],
                  task_state=result["OS-EXT-STS:task_state"], vm_state=result["OS-EXT-STS:vm_state"],
                  volume=result["os-extended-volumes:volumes_attached"], locked=result["locked"],
                  addresses=result["addresses"], hostId=result["hostId"], tags=result["tags"])


class ServerManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, owner=None, identification=None):
        list_result = []
        # TODO(dc): system user access nova
        # if self.user.flag == 'sys':
        #     result = requests.get(self.user.endpoint['nova'], data=None,
        #                           headers=self.user.headers).json()
        #     for i in range(len(result["servers"])):
        #         dict_result.append(self.struc_server(result["servers"]))
        #     return dict_result
        if identification is not None:
            result = requests.get(self.user.endpoint['nova'] + '/' + identification, data=None,
                                  headers=self.user.headers).json()
            return list_result.append(struc_server(result["server"]))
        result = requests.get(self.user.endpoint['nova'] + '/detail', data=None, headers=self.user.headers).json()
        if owner is None:
            for i in range(len(result["servers"])):
                list_result.append(struc_server(result["servers"][i]))
            return list_result
        for i in range(len(result["servers"])):
            if owner == result["servers"][i]["description"]:
                list_result.append(struc_server(result["servers"][i]))
        return list_result

    def create(self, **kwargs):
        params = {
            "server": {
                "networks": [],
                "block_device_mapping_v2": [{"boot_index": "0"}]
            }
        }
        params["server"]["name"] = kwargs["name"]
        params["server"]["flavorRef"] = kwargs["flavorRef"]
        params["server"]["networks"].append({"uuid": kwargs["net_uuid"]})

        params["server"]["block_device_mapping_v2"][0]["source_type"] = kwargs["source_type"]
        params["server"]["block_device_mapping_v2"][0]["destination_type"] = kwargs["destination_type"]
        if kwargs.get("source_uuid"):
            params["server"]["block_device_mapping_v2"][0]["uuid"] = kwargs["source_uuid"]
        if kwargs.get("delete_on_termination"):
            params["server"]["block_device_mapping_v2"][0]["delete_on_termination"] = kwargs["delete_on_termination"]
        if kwargs.get("volume_size"):
            params["server"]["block_device_mapping_v2"][0]["volume_size"] = kwargs["volume_size"]
        if kwargs.get("destination_type"):
            params["server"]["block_device_mapping_v2"][0]["destination_type"] = kwargs["destination_type"]

        params["server"]["imageRef"] = kwargs["imageRef"]

        if kwargs.get("OS-DCF:diskConfig"):
            params["server"]["OS-DCF:diskConfig"] = kwargs["OS-DCF:diskConfig"]
        if kwargs.get("security_groups"):
            params["server"]["security_groups"] = kwargs["security_groups"]
        if kwargs.get("description"):
            params["server"]["description"] = kwargs["description"]
        if kwargs.get("metadata"):
            params["server"]["metadata"] = kwargs["metadata"]

        result = requests.post(self.user.endpoint['nova'], data=params, headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        params = {
            "server": {
            }
        }
        if kwargs.get("name"):
            params["server"]["name"] = kwargs["name"]
        if kwargs.get("description"):
            params["server"]["description"] = kwargs["description"]
        if kwargs.get("OS-DCF:diskConfig"):
            params["server"]["OS-DCF:diskConfig"] = kwargs["OS-DCF:diskConfig"]
        result = requests.put(self.user.endpoint['nova'] + identification, data=params, headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint['nova'] + identification, headers=self.user.headers)
        return utils.answer_detect(result)

    def manipulate_without_params(self, action, identification):
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
        result = requests.post(self.user.endpoint['nova'] + '/' + identification + '/action',
                               data=json.dumps(action_set[action]), headers=self.user.headers)
        return utils.answer_detect(result)

    def manipulate_with_params(self, action, identification, **kwargs):
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
        result = requests.post(self.user.endpoint['nova'] + identification, data=json.dumps(action_set[action]),
                               headers=self.user.headers)
        return utils.answer_detect(result)


class Server(object):
    def __init__(self, name, identification, created, updated,
                 description, flavor_obj, image, key_name,  # metadata,
                 security_groups, status, task_state, vm_state,
                 volume, locked, addresses, hostId, tags):
        self.name = name
        self.identification = identification
        self.created = created
        self.updated = updated
        self.description = description
        self.addresses = addresses
        self.flavor = flavor_obj
        self.image = image
        self.key_name = key_name
        # self.metadata = metadata
        self.security_groups = security_groups
        self.status = status
        self.task_state = task_state
        self.vm_state = vm_state
        self.volume = volume
        self.locked = locked
        self.hostId = hostId
        self.tags = tags
