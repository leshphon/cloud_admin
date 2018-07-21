# coding=utf-8
import warnings

import networks
import subnet
import port
import router
import floatip

class Client(object):

    def __init__(self):
        self.client_name = 'Neutron'

    @staticmethod
    def get_network():
        network_manager = networks.NetworkManager()
        network_manager.