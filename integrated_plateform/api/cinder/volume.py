# coding=utf-8
import requests
import json

import utils


class VolumeManager(object):
    def __init__(self, user):
        self.user = user

    def get(self):
        result = requests.get(self.user.endpoint["cinder"] + '/' + self.user.project.identification +
                              '/volumes/detail', headers=self.user.headers)
        return utils.answer_detect(result)

# TODO(dc): create, update and delete

# TODO(dc): Volume actions and Volume snapshots
