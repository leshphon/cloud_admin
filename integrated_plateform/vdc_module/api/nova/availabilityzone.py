# coding=utf-8
import vdc_module.api.detect as detect
import json
import requests
import base


def show(user):
    temp_url = base.url.get_nova("availabilityZones") + '/detail'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.post(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)
