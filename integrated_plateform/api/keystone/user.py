# coding=utf-8
import requests
import json
import warnings

import utils


class UserManager(object):
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
        self.__users_url = utils.get_endpoint(self.token, 'keystone') + '/users'

    def create(self, project, name, passwd, role, **kwargs):
        params = {
            "user": {
                "name": name,
                "password": passwd,
                "default_project_id": project.identification,
                "enabled": True,
            }
        }
        # TODO(dc):description is not concerned
        # if kwargs.get("description"):
        #     params["user"]["description"] = kwargs.get("description")
        if kwargs.get("domain_id"):
            params["user"]["domain_id"] = kwargs.get("domain_id")
        user_id = json.loads(requests.post(url=self.__users_url, data=json.dumps(params),
                                           headers=self.__headers).content)["user"]["id"]
        # TODO(dc): domain is not concerned
        requests.put(url=utils.get_endpoint(self.token, 'keystone') +
                     '/projects/' + project.identification + '/users/' + user_id + '/roles/' +
                     role.identification, headers=self.__headers)
        return self.get(name=name, passwd=passwd, project=project)

    def get(self, name=None, passwd=None, project=None, flag='non-sys', domain='default'):
        if flag != 'non-sys' and flag != 'sys':
            print("wrong user flag")
            return None
        return User(name=name, passwd=passwd, project=project, domain=domain, flag=flag)


class User(object):
    def __init__(self, name=None, passwd=None, project=None, flag='non-sys', domain='default'):
        self.__users_url = ('http://' + utils.init_data().get('host', 'IP') + ':' +
                            utils.init_data().get('keystone', 'PORT') + '/' +
                            utils.init_data().get('keystone', 'VERSION') + '/users')
        self.flag = flag
        self.domain = domain
        self.name = name
        self.passwd = passwd
        self.project = project

        self.identification = None
        self.enable = False
        self.endpoint = {}
        # TODO(dc) user quota
        # TODO(dc) self.quota = None
        self.token = utils.get_token(self)
        self.headers = {
            'User-Agent': utils.init_data().get('agent', 'ALL'),
            'X-Auth-Token': self.token,
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        self._set_info()

    def _set_info(self):
        """"""
        if self.token is None:
            return None
        result = requests.get(url=self.__users_url, data=None, headers=self.headers)
        dict_result = json.loads(result.content)
        for i in range(len(dict_result['users'])):
            if dict_result['users'][i]['name'] == self.name:
                self.identification = dict_result['users'][i]['id']
                break
            elif i == len(dict_result['users']) - 1:
                """Record error info"""
                self.identification = None
                warnings.warn('No this user!', Warning)
            else:
                continue
        result = requests.get(url=self.__users_url + '/' + self.identification, data=None, headers=self.headers)
        dict_result = json.loads(result.content)
        self.enable = dict_result['user']['enabled']
        self.endpoint["keystone"] = utils.get_endpoint(self.token, "keystone")
        self.endpoint["nova"] = utils.get_endpoint(self.token, "nova")
        self.endpoint["cinder"] = utils.get_endpoint(self.token, "cinder")
        self.endpoint["glance"] = utils.get_endpoint(self.token, "glance")
        self.endpoint["neutron"] = utils.get_endpoint(self.token, "neutron")
        # TODO(dc) set user quota
        # TODO(dc) self.quota is not concerned
