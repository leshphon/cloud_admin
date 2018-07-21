# coding=utf-8
import warnings
import json
from copy import deepcopy

import image


class Client(object):
    def __init__(self):
        self.client_name = 'Glance'

    @staticmethod
    def create_image(user, upload_file, params):
        image_manager = image.ImageManager(user=user)
        result = image_manager.create(**params)
        if not isinstance(result, dict):
            result = json.loads(result)
        if result['detect']['code'] == 0:
            return result
        result = image_manager.upload(identification=result['id'], upload_file=upload_file)
        if not isinstance(result, dict):
            result = json.loads(result)
        if result['detect']['code'] == 0:
            image_manager.delete(identification=result['id'])
        return result

    @staticmethod
    def show_image(user, identification=None):
        image_manager = image.ImageManager(user=user)
        result = image_manager.get(identification=identification)
        if not isinstance(result, dict):
            result = json.loads(result)
        if result["detect"]["code"] == 1:
            new_list = deepcopy(result["images"])
            for i in new_list:
                if i["owner"] != user.project.identification:
                    result["images"].remove(i)
            return json.dumps(result)
        else:
            return json.dumps(result)

    @staticmethod
    def update_image(user, identification, params):
        image_manager = image.ImageManager(user=user)
        result = image_manager.update(identification=identification, **params)
        if user.project.identification != json.loads(result)["owner"]:
            return json.dumps({'detect': {"msg": "ErrorAuth", "code": 0}})
        return result

    @staticmethod
    def delete_image(user, identification):
        image_manager = image.ImageManager(user=user)
        if user.project.identification != json.loads(image_manager.get(identification=identification))["owner"]:
            return json.dumps({'detect': {"msg": "ErrorAuth", "code": 0}})
        return image_manager.delete(identification=identification)