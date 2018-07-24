# coding=utf-8
import requests
import json

import utils


class PortManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None, **kwargs):
        url = self.user.endpoint['neutron'] + '/ports'
        if identification is None:
            if kwargs.get("network_id") is not None:
                url = url + "?network_id=" + kwargs["network_id"]
            result = requests.get(url=url, data=None, headers=self.user.headers)
        else:
            result = requests.get(url=url + '/' + identification, data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        url = self.user.endpoint['neutron'] + '/ports'
        params = {
            "port": {
                "network_id": kwargs.get("network_id"),
                "fixed_ips": [{}]
            }
        }
        if kwargs.get("subnet_id") is not None:
            params["port"]["fixed_ips"][0]["subnet_id"] = kwargs.get("subnet_id")
        if kwargs.get("ip_address") is not None:
            params["port"]["fixed_ips"][0]["ip_address"] = kwargs.get("ip_address")
        result = requests.post(url=url, data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)
