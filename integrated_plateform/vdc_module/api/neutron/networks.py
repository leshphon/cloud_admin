import vdc_module.api.detect as detect
import requests
import base
import json


def show(user):
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.get(base.url.get_neutron("networks"), data=None, headers=headers)
    return detect.ansDetection(result)
