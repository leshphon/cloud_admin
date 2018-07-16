# coding=utf-8
import requests
import json
import base
from vdc_module.api.member import User, Token


def show(user):
    # list project with token
    pj_r = requests.get(base.url.get_keystone("project"), headers={"X-Auth-Token": user.token.unscoped_token_value})
    pj_info = json.loads(pj_r.text)
    pj_list = {}
    pj_num = len(pj_info['projects'])
    for num in range(pj_num):
        pj_list[num] = {'name': pj_info['projects'][num]['name'], 'id': pj_info['projects'][num]['id']}
    return pj_list
