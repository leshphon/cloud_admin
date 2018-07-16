# coding=utf-8
import json
import vdc_module.api.detect as detect
import requests
import base


def show(user, server_id):
    # Normal response codes: 200
    # Error response codes: unauthorized(401), forbidden(403), itemNotFound(404)
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/metadata'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.get(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def delete(user, server_id, keyname):
    # Normal response codes: 204
    # Error response codes: unauthorized(401), forbidden(403), itemNotFound(404), conflict(409)
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/metadata' + keyname
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.delete(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def create(user, server_id, info):
    # Normal response codes: 200
    # Error response codes: badRequest(400), unauthorized(401), forbidden(403), itemNotFound(404), conflict(409)
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/metadata'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    params = base.mapping.info2params(info, base.mapping.nova_create_servermeta_key2key,
                                      base.mapping.nova_create_servermeta_key2path)
    result = requests.put(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)
