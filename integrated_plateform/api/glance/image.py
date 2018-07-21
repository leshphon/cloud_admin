# coding=utf-8
import requests
import json

import utils


class ImageManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification=None):
        if identification is not None:
            result = requests.get(self.user.endpoint["glance"] + '/images/' + identification, headers=self.user.headers)
            return utils.answer_detect(result)
        result = requests.get(self.user.endpoint["glance"] + '/images', headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, **kwargs):
        params = {"name": kwargs["name"], "disk_format": kwargs["disk_format"]}

        if kwargs.get("container_format"):
            params["container_format"] = kwargs["container_format"]
        if kwargs.get("min_disk"):
            params["min_disk"] = kwargs["min_disk"]
        if kwargs.get("min_ram"):
            params["min_ram"] = kwargs["min_ram"]
        if kwargs.get("protected"):
            params["protected"] = kwargs["protected"]
        if kwargs.get("visibility"):
            params["visibility"] = kwargs["visibility"]
        if kwargs.get("tags"):
            params["tags"] = kwargs["tags"]
        result = requests.post(url=self.user.endpoint['glance'] + '/images', data=json.dumps(params),
                               headers=self.user.headers)
        return utils.answer_detect(result, flag='dict')

    def upload(self, upload_file, identification):
        headers = {
            'X-Auth-Token': self.user.token,
            "Content-type": "application/octet-stream"
        }

        result = requests.put(url=self.user.endpoint['glance'] + '/images/' + identification + '/file',
                              headers=headers, data=upload_file)
        return utils.answer_detect(result)

    def update(self, identification, **kwargs):
        headers = {
            'X-Auth-Token': self.user.token,
            "Content-type": "application/openstack-images-v2.1-json-patch"
        }
        params = []

        if kwargs.get("name"):
            params.append({"op": "replace", "path": "/name", "value": kwargs["name"]})

        if kwargs.get("protected"):
            params.append({"op": "replace", "path": "/protected", "value": kwargs["protected"]})

        if kwargs.get("visibility"):
            params.append({"op": "replace", "path": "/visibility", "value": kwargs["visibility"]})
        result = requests.patch(url=self.user.endpoint['glance'] + '/images/' + identification, data=json.dumps(params),
                                headers=headers)
        return utils.answer_detect(result)

    def delete(self, identification):
        result = requests.delete(url=self.user.endpoint['glance'] + '/images/' + identification,
                                 headers=self.user.headers)
        return utils.answer_detect(result)
