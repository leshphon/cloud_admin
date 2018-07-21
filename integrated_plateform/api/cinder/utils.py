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
    return "".join([random.choice(string.letters + string.digits + '!@#$%^&*()_+={}[]\/~`') for i in range(key_len)])


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






