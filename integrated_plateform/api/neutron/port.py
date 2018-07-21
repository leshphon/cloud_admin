# coding=utf-8
import requests
import json

import utils


class PortManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None):
        if identification is None:
            result = requests.get(self.user.endpoint['neutron'] + '/ports', data=None, headers=self.user.headers)
        else:
            result = requests.get(self.user.endpoint['neutron'] + '/ports/' + identification,
                                  data=None, headers=self.user.headers)
        return utils.answer_detect(result)