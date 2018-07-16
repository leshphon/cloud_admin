# coding=utf-8
import requests
import json
import base
from vdc_module.api.member import User, Token


def unscpoed(user):
    # Password authentication with unscoped authorization
    headers = {
        'User-Agent': base.user_agent,
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    info = {
        "domain_name": user.domain.current_domain,
        "password": user.password,
        "user_name": user.username,
        "methods": "password"
    }

    params = base.mapping.info2params(info, base.mapping.keystone_unscoped_key2key,
                                      base.mapping.keystone_unscoped_key2path)

    result = requests.post(base.url.get_keystone("token"), data=params, headers=headers)

    if result.status_code == 201:
        x_sub_token = result.headers['X-Subject-Token']
        user.token.unscoped_token_value = x_sub_token
        user.token.unscoped_token_id = x_sub_token
    return user


def scoped(user):
    # Password authentication with scoped authorization
    headers = {
        'User-Agent': base.user_agent,
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    info = {
        "project_domain_name": user.domain.current_domain,
        "project_name": user.project.currentpj['name'],
        "user_domain_name": user.domain.current_domain,
        "password": user.password,
        "user_name": user.username,
        "methods": "password"
    }
    params = base.mapping.info2params(info, base.mapping.keystone_scoped_key2key, base.mapping.keystone_scoped_key2path)
    result = requests.post(base.url.get_keystone("token"), data=params, headers=headers)

    x_auth_token = result.headers['X-Subject-Token']
    user.token.scoped_token_value = x_auth_token
    user.token.scoped_token_id = x_auth_token

    role_id = json.loads(result.text)['token']['roles'][0]['id']
    role_name = json.loads(result.text)['token']['roles'][0]['name']
    endpoint = json.loads(result.text)['token']['catalog']
    user_id = json.loads(result.text)['token']['user']['id']

    user.role.current_role_id = role_id
    user.role.current_role_name = role_name
    user.endpoint = endpoint
    user.user_id = user_id
    return user


def check(user):
    check_result = requests.head(base.url.get_keystone("token"),
                                 headers={"X-Auth-Token": user.token.scoped_token_value,
                                          "X-Subject-Token": user.token.scoped_token_value})
    if check_result.status_code == 200:
        return user
    else:
        user = User()
        user.enabled = False
        return user



