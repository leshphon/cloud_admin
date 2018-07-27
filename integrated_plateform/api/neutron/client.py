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

    # network
    @staticmethod
    def get_network(user, identification=None):
        network_manager = networks.NetworkManager(user=user)
        if user.flag == 'non-sys':
            params = {
                "project_id": user.project.identification
            }
            return network_manager.get(identification=identification, **params)
        elif user.flag == 'sys':
            return network_manager.get(identification=identification)

    @staticmethod
    def create_network(user, params):
        network_manager = networks.NetworkManager(user=user)
        return network_manager.create(**params)

    @staticmethod
    def update_network(user, identification, params):
        network_manager = networks.NetworkManager(user=user)
        return network_manager.update(identification=identification, **params)

    @staticmethod
    def delete_network(user, identification):
        network_manager = networks.NetworkManager(user=user)
        return network_manager.delete(identification=identification)

    # subnet
    @staticmethod
    def get_subnet(user, params=None, identification=None):
        subnet_manager = subnet.SubnetManager(user=user)
        return subnet_manager.get(identification=identification, **params)

    @staticmethod
    def create_subnet(user, params):
        subnet_manager = subnet.SubnetManager(user=user)
        return subnet_manager.create(**params)

    @staticmethod
    def update_subnet(user, identification, params):
        subnet_manager = subnet.SubnetManager(user=user)
        return subnet_manager.update(identification=identification, **params)

    @staticmethod
    def delete_subnet(user, identification):
        subnet_manager = subnet.SubnetManager(user=user)
        return subnet_manager.delete(identification=identification)

    # port
    @staticmethod
    def get_port(user, params=None, identification=None):
        port_manager = port.PortManager(user=user)
        return port_manager.get(identification=identification, **params)

    @staticmethod
    def create_port(user, params=None):
        port_manager = port.PortManager(user=user)
        return port_manager.create(**params)
