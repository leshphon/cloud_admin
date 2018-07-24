# coding=utf-8
import json
import requests

import utils


class MetadataManager(object):
    def __init__(self, user):
        self.user = user

    def get(self, identification):
        url = self.user.endpoint["nova"] + "/servers/" + identification + "/metadata"
        result = requests.get(url=url, data=None, headers=self.user.headers)
        return utils.answer_detect(result)

    def create(self, identification, **kwargs):
        url = self.user.endpoint["nova"] + "/servers/" + identification + "/metadata"
        params = {
            "metadata": {
                "owner": kwargs.get("owner")
            }
        }
        result = requests.get(url=url, data=json.dumps(params), headers=self.user.headers)
        return utils.answer_detect(result)
