# coding=utf-8
import random
import string
import os
import ConfigParser
import json
import requests
import warnings


def rstr_gen(key_len):
    """
    :param key_len: the length of targeted random dig or str
    :return:
    """
    return "".join([random.choice(string.letters + string.digits + '!@#$%^&*_+=~`') for i in range(key_len)])


def answer_detect(result, flag="JSON"):
    """Detect the openstack result of JSON
    :param result: the full openstack JSON ans
    :param flag: JSON or dict
    :return: full openstack JSON ans with additional detect info and format is like below:
            {  openstack result info
              "detect": {"msg": "Normal", "code": 1}
              }
    """
    send = {}
    status = {
        200: "Normal",
        201: "Normal",
        202: "Normal",
        204: "Normal",
        400: "ErrorBadRequest",
        401: "ErrorUnauthorized",
        403: "ErrorForbidden",
        404: "ErrorItemNotFound",
        409: "ErrorConflict"
    }
    send['msg'] = status.get(result.status_code, "OtherError")
    if send['msg'] == "Normal":
        send['code'] = 1
    else:
        send['code'] = 0
    try:
        temp = json.loads(result.content)
    except:
        temp = {}
    temp['detect'] = send
    if flag == "JSON":
        return json.dumps(temp)
    elif flag == "dict":
        return temp
    else:
        warnings.warn("Wrong format chosen!")
        return None


def init_data():
    cp_ini = ConfigParser.SafeConfigParser(allow_no_value=False)
    cp_ini.read(os.path.abspath(os.path.dirname(__file__)) + '/' + 'config.ini')
    return cp_ini


def get_endpoint(token, service_name):
    headers = {
        'User-Agent': init_data().get('agent', 'ALL'),
        'X-Auth-Token': token,
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    result = requests.get(url='http://' + init_data().get('host', 'IP') + ':' + init_data().get(service_name, 'PORT'),
                          headers=headers)
    endpoint = []
    parse_result(result.json(), endpoint)
    return endpoint[0]


def parse_result(input_dict, endpoint):
    endpoint_status = ''
    if isinstance(input_dict, dict):
        for json_result in input_dict.values():
            if 'status' in input_dict.keys():
                # print key
                endpoint_status = input_dict.get('status')
            else:
                parse_result(json_result, endpoint)
    elif isinstance(input_dict, list):
        for json_array in input_dict:
            parse_result(json_array, endpoint)
    if endpoint_status == "stable" or endpoint_status == "CURRENT":
        for i in range(len(input_dict["links"])):
            if input_dict["links"][i]["rel"] == 'self':
                endpoint += [input_dict["links"][i]["href"]]
                break


def get_token(user=None):
    headers = {
        'User-Agent': init_data().get('agent', 'ALL'),
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    token_url = ('http://' + init_data().get('host', 'IP') + ':' + init_data().get('keystone', 'PORT') + '/' +
                 init_data().get('keystone', 'VERSION') + '/auth/tokens')

    if user is None:
        params = {"auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": init_data().get('host', 'DOMAIN')
                        },
                        "name": init_data().get('host', 'ADMIN'),
                        "password": init_data().get('host', 'PASSWD')
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": init_data().get('host', 'DOMAIN')
                    },
                    "name": init_data().get('host', 'PROJECT')
                }
            }}}
    else:
        params = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "domain": {
                                "name": user.domain
                            },
                            "name": user.name,
                            "password": user.passwd
                        }
                    }
                },
                "scope": {
                    "project": {
                        "domain": {
                            "name": user.domain
                        },
                        "name": user.project.name
                    }
                }}}
    result = requests.post(token_url, data=json.dumps(params), headers=headers)
    if answer_detect(result, flag='dict')['detect']['code'] == 1:
        return result.headers['X-Subject-Token']
    else:
        return None


def revoke_obj(obj):
    if obj.token is None:
        # print("Token is None, obj has been revoked")
        return None
    headers = {
        "X-Auth-Token": obj.token,
        "X-Subject-Token": obj.token
    }
    token_url = ('http://' + init_data().get('host', 'IP') + ':' + init_data().get('keystone', 'PORT') + '/' +
                 init_data().get('keystone', 'VERSION') + '/auth/tokens')
    result = requests.delete(url=token_url, headers=headers)
    if answer_detect(result, flag='dict')['detect']['code'] == 1:
        return None
    else:
        warnings.warn("Revoke_obj error")


