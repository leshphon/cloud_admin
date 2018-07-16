# coding=utf-8
import json
import vdc_module.api.detect as detect
import requests
import base


# key pairs actions
def show(user):
    # Normal response codes: 200
    # Error response codes: unauthorized(401), forbidden(403)
    temp_url = base.url.get_nova("keyPair")
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.get(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def create(user, info):
    # Normal response codes: 200, 201
    # Error response codes: badRequest(400), unauthorized(401), forbidden(403), conflict(409)
    temp_url = base.url.get_nova("keyPair")
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    params = base.mapping.info2params(info, base.mapping.nova_create_keypairs_key2key,
                                      base.mapping.nova_create_keypairs_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def details(user, keypair_name):
    # Normal response codes: 200
    # Error response codes: unauthorized(401), forbidden(403), itemNotFound(404)
    temp_url = base.url.get_nova("keyPair") + keypair_name
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.get(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def delete(user, keypair_name):
    # Normal response codes: 202, 204
    # Error response codes: unauthorized(401), forbidden(403), itemNotFound(404)
    temp_url = base.url.get_nova("keyPair") + keypair_name
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.delete(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)
