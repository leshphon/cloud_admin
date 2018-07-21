# coding=utf-8
import requests
import json
import warnings

import utils


class RoleManager(object):
    """

    """

    def __init__(self):
        self.token = utils.get_token()
        self.enable = True
        self.__headers = {
            'User-Agent': utils.init_data().get('agent', 'ALL'),
            'X-Auth-Token': self.token,
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        self.__roles_url = utils.get_endpoint(self.token, 'keystone') + '/roles'

    def create(self, name, **kwargs):
        # TODO not concerned
        pass

    def get(self, name=None):
        try:
            if name is None:
                return requests.get(url=self.__roles_url, headers=self.__headers)
            else:
                result = requests.get(url=self.__roles_url, headers=self.__headers)
                dict_result = json.loads(result.content)
                for i in range(len(dict_result['roles'])):
                    if dict_result['roles'][i]['name'] == name:
                        return Role(name=name, identification=dict_result['roles'][i]['id'])
                    elif i == len(dict_result['roles']) - 1:
                        """Record error info"""
                        warnings.warn('No this role!', Warning)
                    else:
                        continue
        except KeyError:
            '''Record error!'''
            warnings.warn('No params!', Warning)


class Role(object):
    def __init__(self, name, identification):
        self.name = name
        self.identification = identification
