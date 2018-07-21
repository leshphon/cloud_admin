# coding=utf-8
import json
import requests

import utils


def struct_flavor(result):
    return Flavor(name=result["name"], ram=result["ram"], vcpus=result["vcpus"], disk=result["disk"],
                  identification=result["identification"], description=result["description"])


class FlavorManager(object):
    def __init__(self, user):
        self.user = user

    def get(self):
        list_result = []
        result = requests.get(self.user.endpoint["nova"] + '/flavors/detail', headers=self.user.headers).json()
        for i in range(len(result)):
            list_result.append(struct_flavor(result["flavors"][i]))

    def create(self, **kwargs):
        params = {
            "flavor": {}
        }
        params["flavor"]["name"] = kwargs["name"]
        params["flavor"]["ram"] = kwargs["ram"]
        params["flavor"]["vcpus"] = kwargs["vcpus"]
        params["flavor"]["disk"] = kwargs["disk"]
        if kwargs.get("description"):
            params["flavor"]["description"] = kwargs["description"]
        if kwargs.get("id"):
            params["flavor"]["id"] = kwargs["identification"]
        result = requests.post(self.user.endpoint["nova"] + '/flavors', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint["nova"] + '/flavors/' + identification,
                                 headers=self.user.headers)
        return utils.answer_detect(result)


class Flavor(object):
    def __init__(self, name, ram, vcpus, disk, identification, description):
        self.name = name
        self.ram = ram
        self.vcpus = vcpus
        self.disk = disk
        self.identification = identification
        self.description = description
