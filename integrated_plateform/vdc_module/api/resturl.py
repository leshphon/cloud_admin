# coding=utf-8
import os
import ConfigParser

cp_ini = ConfigParser.SafeConfigParser(allow_no_value=False)
cp_ini.read(os.path.abspath(os.path.dirname(__file__)) + '/' + 'config.ini')


class Url(object):

    def __init__(self):
        host_ip = cp_ini.get('host', 'IP')
        # keystone url
        self.__keystone_base_url = 'http://' + host_ip + ':' + cp_ini.get('keystone', 'PORT')
        self.__keystone_token_url = self.__keystone_base_url + '/' + cp_ini.get('keystone', 'VERSION') + '/auth/tokens'
        self.__available_project_scopes_url = self.__keystone_base_url + '/' + cp_ini.get('keystone',
                                                                                          'VERSION') + '/auth/projects'
        self.__service_catalog_url = self.__keystone_base_url + '/' + cp_ini.get('keystone',
                                                                                 'VERSION') + '/auth/catalog'
        self.__available_domain_scopes_url = self.__keystone_base_url + '/' + cp_ini.get('keystone',
                                                                                         'VERSION') + '/auth/domains'
        self.__service_url = self.__keystone_base_url + '/' + cp_ini.get('keystone', 'VERSION') + '/services'
        # keystone action
        self.__keystone_action = {
            "token": self.__keystone_token_url,
            "project": self.__available_project_scopes_url,
            "catalog": self.__service_catalog_url,
            "domain": self.__available_domain_scopes_url,
            "service": self.__service_url
        }

        # nova url
        self.__compute_base_url = 'http://' + host_ip + ':' + cp_ini.get('nova', 'PORT')
        self.__nova_server_url = self.__compute_base_url + '/' + cp_ini.get('nova', 'VERSION') + '/servers'
        self.__nova_flavor_url = self.__compute_base_url + '/' + cp_ini.get('nova', 'VERSION') + '/flavors'
        self.__nova_keypair_url = self.__compute_base_url + '/' + cp_ini.get('nova', 'VERSION') + '/os-keypairs'
        self.__nova_availabilityzone_url = self.__compute_base_url + '/' + cp_ini.get('nova', 'VERSION') + \
                                           '/os-availability-zone'
        # nova action
        self.__nova_action = {
            'servers': self.__nova_server_url,
            'flavors': self.__nova_flavor_url,
            'keyPair': self.__nova_keypair_url,
            'availabilityZones': self.__nova_availabilityzone_url
        }

        # neutron url
        self.__neutron_base_url = 'http://' + host_ip + ':' + cp_ini.get('neutron', 'PORT')
        self.__networks_url = self.__neutron_base_url + '/' + cp_ini.get('neutron', 'VERSION') + '/networks'
        # neutron action
        self.__neutron_action = {
            'networks': self.__networks_url
        }

        # glance url
        self.__glance_base_url = 'http://' + host_ip + ':' + cp_ini.get('glance', 'PORT')
        self.__images_url = self.__glance_base_url + '/' + cp_ini.get('glance', 'VERSION') + '/images'
        # glance action
        self.__glance_action = {
            'images': self.__images_url
        }

        # cinder url
        self.__cinder_base_url = 'http://' + host_ip + ':' + cp_ini.get('cinder', 'PORT')
        self.__volume_url = self.__cinder_base_url + '/' + cp_ini.get('cinder', 'VERSION')
        # cinder action
        self.__cinder_action = {
            'volume': self.__volume_url
        }

    def get_keystone(self, params):
        try:
            return self.__keystone_action[params]
        except ValueError, e:
            print e

    def get_nova(self, params):
        try:
            return self.__nova_action[params]
        except ValueError, e:
            print e

    def get_neutron(self, params):
        try:
            return self.__neutron_action[params]
        except ValueError, e:
            print e

    def get_glance(self, params):
        try:
            return self.__glance_action[params]
        except ValueError, e:
            print e

    def get_cinder(self, params):
        try:
            return self.__cinder_action[params]
        except ValueError, e:
            print e
