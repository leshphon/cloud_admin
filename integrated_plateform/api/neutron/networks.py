# coding=utf-8
import requests
import json

import utils


class NetworkManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None):
        if identification is None:
            result = requests.get(self.user.endpoint['neutron'] + '/networks', data=None, headers=self.user.headers)
        else:
            result = requests.get(self.user.endpoint['neutron'] + '/networks/' + identification,
                                  data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        params = {
            "network": {}
        }
        if kwargs.get("name"):
            params["network"]["name"] = kwargs["name"]
        # if kwargs.get("dns_domain"):
        #     params["network"]["dns_domain"] = kwargs["dns_domain"]
        if kwargs.get("project_id"):
            params["network"]["project_id"] = kwargs["project_id"]
        if kwargs.get("provider:network_type"):
            params["network"]["provider:network_type"] = kwargs["provider:network_type"]
        if kwargs.get("provider:physical_network"):
            params["network"]["provider:physical_network"] = kwargs["provider:physical_network"]
        if kwargs.get("shared"):
            params["network"]["shared"] = kwargs["shared"]
        if kwargs.get("description"):
            params["network"]["description"] = kwargs["description"]
        result = requests.post(self.user.endpoint['neutron'] + '/networks', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        params = {
            "network": {}
        }
        if kwargs.get("name"):
            params["network"]["name"] = kwargs["name"]
        if kwargs.get("dns_domain"):
            params["network"]["dns_domain"] = kwargs["dns_domain"]
        result = requests.put(self.user.endpoint['neutron'] + '/networks/' + identification,
                              data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint['neutron'] + '/networks/' + identification,
                                 data=None, headers=self.user.headers)
        return utils.answer_detect(result)
