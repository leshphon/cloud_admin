# coding=utf-8
import requests
import json
import warnings

import utils


class ProjectManger(object):
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
        self.__projects_url = utils.get_endpoint(self.token, 'keystone') + '/projects'

    def get(self, name=None, identification=None):
        """

        :param name:
        :param identification:
        :return:
        """
        if name is not None and identification is None:
            result = requests.get(url=self.__projects_url, data=None, headers=self.__headers)
            dict_result = json.loads(result.content)
            identification = ''
            for i in range(len(dict_result['projects'])):
                if dict_result['projects'][i]['name'] == name:
                    identification = dict_result['projects'][i]['id']
                    break
                elif i == len(dict_result['projects']) - 1:
                    """Record error info"""
                    identification = None
                    warnings.warn('No this project!', Warning)
                else:
                    continue
        result = requests.get(url=self.__projects_url + '/' + identification, data=None, headers=self.__headers)
        dict_result = json.loads(result.content)
        description = dict_result['project']['description']
        enable = dict_result['project']['enabled']
        return Project(name=name, identification=identification, description=description, enable=enable)

    def create(self, name, **kwargs):
        """Create a openstack project
        :param name: vdc info from frontend which will be encoded
        :param kwargs: additional attribute just like description,domain_id
        :return: opensatck back result of this created project with JSON format
        """
        try:
            params = {
                "project": {
                    "name": name,
                    "enabled": True,
                    "is_domain": False,
                }
            }
            if kwargs.get("description"):
                params["project"]["description"] = kwargs.get("description")
            if kwargs.get("domain_id"):
                params["project"]["domain_id"] = kwargs.get("domain_id")
            requests.post(url=self.__projects_url, data=json.dumps(params), headers=self.__headers)
            return self.get(name=name)
        except KeyError:
            '''Record error!'''
            warnings.warn('Project create wrong!', Warning)

    def update(self, name=None, identification=None, **kwargs):
        """

        :param name:
        :param identification:
        :param kwargs:
        :return:
        """
        try:
            params = {
                "project": {
                }
            }
            if kwargs.get("name"):
                params["project"]["name"] = kwargs.get("name")
            if kwargs.get("description"):
                params["project"]["description"] = kwargs.get("description")
            if kwargs.get("domain_id"):
                params["project"]["domain_id"] = kwargs.get("domain_id")
            if kwargs.get("enabled"):
                params["project"]["enabled"] = kwargs.get("enabled")
            if name is not None and identification is None:
                requests.patch(url=self.__projects_url + '/' + self.get(name=name).identification,
                               data=json.dumps(params), headers=self.__headers)
            if name is None and identification is not None:
                requests.patch(url=self.__projects_url + '/' + identification, data=json.dumps(params),
                               headers=self.__headers)
            else:
                warnings.warn('Project update params wrong!', Warning)
                return None
            return self.get(identification=identification)
        except KeyError:
            '''Record error!'''
            warnings.warn('Project update wrong!', Warning)

    def delete(self, name=None, identification=None):
        """

        :param name:
        :param identification:
        :return:
        """
        try:
            if name is not None and identification is None:
                return requests.delete(url=self.__projects_url + '/' + self.get(name=name).identification,
                                       headers=self.__headers)
            if name is None and identification is not None:
                return requests.delete(url=self.__projects_url + '/' + identification, headers=self.__headers)
            else:
                warnings.warn('Project delete params wrong!', Warning)
                return None
        except KeyError:
            '''Record error!'''
            warnings.warn('Project delete wrong!', Warning)


class Project(object):
    """

    """
    def __init__(self, name, identification, description, enable):
        self.name = name
        self.identification = identification
        self.description = description
        self.enable = enable
        self.token = None
