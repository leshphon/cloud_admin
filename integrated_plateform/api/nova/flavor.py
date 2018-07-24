# coding=utf-8
import json
import requests

import utils


def struct_flavor(result):
    return Flavor(name=result["name"], ram=result["ram"], vcpus=result["vcpus"], disk=result["disk"],
                  identification=result["id"], is_public=result["os-flavor-access:is_public"])


class FlavorManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None, **kwargs):
        if identification is not None:
            result = requests.get(self.user.endpoint["nova"] + '/flavors/detail/' + identification,
                                  headers=self.user.headers)
        else:
            result = requests.get(self.user.endpoint["nova"] + '/flavors/detail' + '?project_id=' +
                                  kwargs.get("project_id"), headers=self.user.headers)
        result_dict = result.json()
        result_len = len(result_dict)
        # This id obj return
        list_result = []
        if utils.answer_detect(result, flag='dict')['detect']['code'] == 1:
            for i in range(result_len):
                list_result.append(struct_flavor(result_dict["flavors"][i]))
            return list_result
        else:
            return utils.answer_detect(result)

    def create(self, **kwargs):
        list_result = []
        params = {
            "flavor": {}
        }
        params["flavor"]["name"] = kwargs["name"]
        params["flavor"]["ram"] = kwargs["ram"]
        params["flavor"]["vcpus"] = kwargs["vcpus"]
        params["flavor"]["disk"] = kwargs["disk"]
        if kwargs.get("id") is not None:
            params["flavor"]["id"] = kwargs["identification"]
        if kwargs.get("os-flavor-access:is_public") is not None:
            params["flavor"]["os-flavor-access:is_public"] = kwargs["os-flavor-access:is_public"]
        result = requests.post(self.user.endpoint["nova"] + '/flavors', data=json.dumps(params),
                               headers=self.user.headers)
        if utils.answer_detect(result, flag='dict')['detect']['code'] == 1:
            return list_result.append(struct_flavor(result.json()["flavor"]))
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint["nova"] + '/flavors/' + identification,
                                 headers=self.user.headers)
        return utils.answer_detect(result)


class Flavor(object):
    def __init__(self, name, ram, vcpus, disk, identification, is_public):
        self.name = name
        self.ram = ram
        self.vcpus = vcpus
        self.disk = disk
        self.identification = identification
        self.is_public = is_public
