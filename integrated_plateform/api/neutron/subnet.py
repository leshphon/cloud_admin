# coding=utf-8
import requests
import json

import utils


class SubnetManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None, **kwargs):
        url = self.user.endpoint['neutron'] + '/subnets'
        if identification is None:
            if kwargs.get("network_id") is not None:
                url = url + "?network_id=" + kwargs["network_id"]
            result = requests.get(url=url, data=None, headers=self.user.headers)
        else:
            result = requests.get(url=url + '/' + identification,
                                  data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        params = {
            "subnet": {}
        }
        params["subnet"]["network_id"] = kwargs["network_id"]
        params["subnet"]["cidr"] = kwargs["cidr"]
        params["subnet"]["ip_version"] = kwargs["ip_version"]

        if kwargs.get("name"):
            params["subnet"]["name"] = kwargs["name"]
        if kwargs.get("enable_dhcp"):
            params["subnet"]["enable_dhcp"] = kwargs["enable_dhcp"]
        if kwargs.get("dns_nameservers"):
            params["subnet"]["dns_nameservers"] = kwargs["dns_nameservers"]
        if kwargs.get("allocation_pools"):
            params["subnet"]["host_routes"] = kwargs["host_routes"]
        if kwargs.get("gateway_ip"):
            params["subnet"]["gateway_ip"] = kwargs["gateway_ip"]
        if kwargs.get("host_routes"):
            params["subnet"]["allocation_pools"] = kwargs["allocation_pools"]
        if kwargs.get("description"):
            params["subnet"]["description"] = kwargs["description"]

        result = requests.post(self.user.endpoint['neutron'] + '/subnets', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        params = {
            "subnet": {}
        }
        if kwargs.get("name"):
            params["subnet"]["name"] = kwargs["name"]
        if kwargs.get("enable_dhcp"):
            params["subnet"]["enable_dhcp"] = kwargs["enable_dhcp"]
        if kwargs.get("dns_nameservers"):
            params["subnet"]["dns_nameservers"] = kwargs["dns_nameservers"]
        if kwargs.get("allocation_pools"):
            params["subnet"]["host_routes"] = kwargs["host_routes"]
        if kwargs.get("gateway_ip"):
            params["subnet"]["gateway_ip"] = kwargs["gateway_ip"]
        result = requests.put(self.user.endpoint['neutron'] + '/subnets/' + identification,
                              data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint['neutron'] + '/subnets/' + identification,
                                 data=None, headers=self.user.headers)
        return utils.answer_detect(result)
