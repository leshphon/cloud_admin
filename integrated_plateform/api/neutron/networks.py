# coding=utf-8
import requests
import json

import utils


class NetworkManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None, **kwargs):
        url = self.user.endpoint['neutron'] + '/networks'
        if identification is None:
            if kwargs.get("project_id"):
                url = url + '?project_id=' + kwargs["project_id"]
            result = requests.get(url=url, data=None, headers=self.user.headers)
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
        if kwargs.get("project_id") is not None:
            params["network"]["project_id"] = kwargs["project_id"]
        if kwargs.get("provider:network_type") is not None:
            params["network"]["provider:network_type"] = kwargs["provider:network_type"]
        if kwargs.get("provider:physical_network") is not None:
            params["network"]["provider:physical_network"] = kwargs["provider:physical_network"]
        if kwargs.get("shared") is not None:
            params["network"]["shared"] = kwargs["shared"]
        if kwargs.get("description") is not None:
            params["network"]["description"] = kwargs["description"]
        result = requests.post(self.user.endpoint['neutron'] + '/networks', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        params = {
            "network": {
            }
        }
        if kwargs.get("name"):
            params["network"]["name"] = kwargs.get("name")
        if kwargs.get("shared") is not None:
            params["network"]["shared"] = kwargs.get("shared")
        result = requests.put(self.user.endpoint['neutron'] + '/networks/' + identification,
                              data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(self.user.endpoint['neutron'] + '/networks/' + identification,
                                 data=None, headers=self.user.headers)
        return utils.answer_detect(result)
