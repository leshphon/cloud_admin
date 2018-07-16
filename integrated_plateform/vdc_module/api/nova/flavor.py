# coding=utf-8
import json
import vdc_module.api.detect as detect
import requests
import base


def show(user, flavor_id):
    temp_url = base.url.get_nova("flavors") + '/detail'
    if flavor_id is not None:
        temp_url = temp_url + flavor_id
    headers = {
        'User-Agent': base.user_agent,
        "X-Auth-Token": user.token.scoped_token_value
    }
    result = requests.get(temp_url, headers=headers)
    return detect.ansDetection(result)


def create(user, info):
    temp_url = base.url.get_nova("flavors")
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value
    }
    params = base.mapping.info2params(info, base.mapping.nova_create_flavors_key2key,
                                      base.mapping.nova_create_flavors_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)
