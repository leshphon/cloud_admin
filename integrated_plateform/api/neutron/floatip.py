# coding=utf-8
import requests
import json

import utils


class FloatIPManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None):
        if identification is None:
            result = requests.get(self.user.endpoint['neutron'] + '/floatingips',
                                  data=None, headers=self.user.headers)
        else:
            result = requests.get(self.user.endpoint['neutron'] + '/floatingips/' + identification,
                                  data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        params = {
            "floatingip": {}
        }

        params["floatingip"]["project_id"] = kwargs["project_id"]
        if kwargs.get("fixed_ip_address"):
            params["floatingip"]["fixed_ip_address"] = kwargs["fixed_ip_address"]
        if kwargs.get("floating_ip_address"):
            params["floatingip"]["fixed_ip_address"] = kwargs["floating_ip_address"]
        if kwargs.get("subnet_id"):
            params["floatingip"]["subnet_id"] = kwargs["subnet_id"]
        if kwargs.get("description"):
            params["floatingip"]["description"] = kwargs["description"]

        result = requests.post(self.user.endpoint['neutron'] + '/floatingips', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        # TODO(dc): not concerned
        pass

    def delete(self, identification):
        result = requests.delete(self.user.endpoint['neutron'] + '/floatingips' + identification,
                                 data=None, headers=self.user.headers)
        return utils.answer_detect(result)