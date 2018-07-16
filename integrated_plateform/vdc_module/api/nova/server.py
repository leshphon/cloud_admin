# coding=utf-8
import vdc_module.api.detect as detect
import json
import requests
import base
import status


def show(user):
    temp_url = base.url.get_nova("servers") + '/detail'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.get(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def create(user, info):
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    params = base.mapping.info2params(info, base.mapping.nova_create_server_key2key,
                                      base.mapping.nova_create_server_key2path)
    result = requests.post(base.url.get_nova("servers"), data=params, headers=headers)
    return detect.ansDetection(result)


def update(user, server_id, info):
    temp_url = base.url.get_nova("servers") + '/' + server_id
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    params = base.mapping.info2params(info, base.mapping.nova_update_server_key2key,
                                      base.mapping.nova_update_server_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def details(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    result = requests.get(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def start(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'  # servers/后加server的id
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "os-start": None
    }
    data = json.dumps(values)
    result = requests.post(temp_url, data=data, headers=headers)
    return detect.ansDetection(result)


def stop(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'  # servers/后加server的id
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "os-stop": None
    }
    data = json.dumps(values)
    result = requests.post(temp_url, data=data, headers=headers)
    return detect.ansDetection(result)


def delete(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    # params为空
    result = requests.delete(temp_url, data=None, headers=headers)
    return detect.ansDetection(result)


def pause(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "pause": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def unpause(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "unpause": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


# Image name should be changed
def snapshot(user, server_id, info):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    params = base.mapping.info2params(info, base.mapping.nova_snapshot_key2key,
                                      base.mapping.nova_snapshot_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def migrate(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "migrate": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


# host_id should be changed
def livemigrate(user, server_id, host_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "os-migrateLive": {
            "host": host_id,
            "block_migration": "auto",
            "force": False
        }
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def suspend(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "suspend": None
    }
    params = json.dumps(values)
    print params
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def unsuspend(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "resume": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def lock(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "lock": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def unlock(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "unlock": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def shelve(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "shelve": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def unshelve(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "unshelve": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def shelfOffload(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "shelveOffload": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def hardreboot(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    mode = "HARD"
    values = {
        "reboot": {
            "type": mode
        }
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def softreboot(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    mode = "SOFT"
    values = {
        "reboot": {
            "type": mode
        }
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def rebuild(user, server_id, info):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    params = base.mapping.info2params(info, base.mapping.nova_rebuild_server_key2key,
                                      base.mapping.nova_rebuild_server_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def resize(user, server_id, info):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    params = base.mapping.info2params(info, base.mapping.nova_resize_server_key2key,
                                      base.mapping.nova_resize_server_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def revertResized(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "revertResize": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def confirmResized(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "confirmResize": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def rescue(user, server_id, info):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    params = base.mapping.info2params(info, base.mapping.nova_rescue_server_key2key,
                                      base.mapping.nova_rescue_server_key2path)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)


def unrescue(user, server_id):
    temp_url = base.url.get_nova("servers") + '/' + server_id + '/action'
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json',
    }
    values = {
        "unrescue": None
    }
    params = json.dumps(values)
    result = requests.post(temp_url, data=params, headers=headers)
    return detect.ansDetection(result)
