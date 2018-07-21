# coding=utf-8
import warnings

import volume


class Client(object):
    def __init__(self):
        self.client_name = 'Cinder'

    @staticmethod
    def show_volume(user):
        volume_manager = volume.VolumeManager(user=user)
        return volume_manager.get()

    # TODO(dc): create, update and delete

    # TODO(dc): Volume actions and Volume snapshots
