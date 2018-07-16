# coding=utf-8
import vdc_module.api.detect as detect
import requests
import base
import json


def show(user, image_id, value):
    """
    url中，可使用具体属性进行过滤，如：名字、状态、可见性、标签等，也可加入image_id显示细节列表
    也可使用sort对返回的结果进行排序,具体可见rest_api链接
    :param user:
    :param image_id:
    :param value:
    :return:
    """
    temp_url = base.url.get_glance('images')
    headers = {
        'User-Agent': base.user_agent,
        'X-Auth-Token': user.token.scoped_token_value,
        'Content-Type': 'application/json'
    }
    if image_id is None:
        pass
    else:
        temp_url = temp_url + 'id'
    if value is None:
        result = requests.get(temp_url, headers=headers)
    else:
        result = requests.get(temp_url, data=value, headers=headers)
    return detect.ansDetection(result)
