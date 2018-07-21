# coding=utf-8
import requests
import json

import utils


class RouterManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None):
        if identification is None:
            result = requests.get(self.user.endpoint['neutron'] + '/routers', data=None, headers=self.user.headers)
        else:
            result = requests.get(self.user.endpoint['neutron'] + '/routers/' + identification,
                                  data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        params = {
            "router": {}
        }

        if kwargs.get("name"):
            params["router"]["name"] = kwargs["name"]
        if kwargs.get("project_id"):
            params["router"]["project_id"] = kwargs["project_id"]
        if kwargs.get("description"):
            params["router"]["description"] = kwargs["description"]

        result = requests.post(self.user.endpoint['neutron'] + '/routers', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        params = {
            "router": {}
        }

        if kwargs.get("name"):
            params["router"]["name"] = kwargs["name"]
        if kwargs.get("description"):
            params["router"]["description"] = kwargs["description"]

        result = requests.put(self.user.endpoint['neutron'] + '/routers/' + identification,
                              data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint['neutron'] + '/routers/' + identification,
                                 data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def add_interface(self, identification, **kwargs):
        if kwargs.get("subnet_id") or kwargs.get("port_id"):
            result = requests.put(self.user.endpoint['neutron'] + '/routers/' + identification +
                                  '/add_router_interface', data=json.dumps(kwargs), headers=self.user.headers)
            return utils.answer_detect(result)

    def remove_interface(self, identification, **kwargs):
        if kwargs.get("subnet_id") or kwargs.get("port_id"):
            result = requests.put(self.user.endpoint['neutron'] + '/routers/' + identification +
                                  '/remove_router_interface', data=json.dumps(kwargs), headers=self.user.headers)
            return utils.answer_detect(result)