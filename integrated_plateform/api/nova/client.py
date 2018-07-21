# coding=utf-8
import warnings

import server
import flavor


class Client(object):
    def __init__(self):
        self.client_name = 'Nova'

    @staticmethod
    def create_servers(user, params=None):
        server_manager = server.ServerManager(user=user)
        params["description"] = params["owner"]
        return server_manager.create(**params)

    @staticmethod
    def show_servers(user, owner=None, identification=None):
        server_manager = server.ServerManager(user=user)
        return server_manager.get(owner=owner, identification=identification)

    @staticmethod
    def manipulate_servers(user, action=None, identification=None, params=None):
        server_manager = server.ServerManager(user=user)
        if params is None:
            return server_manager.manipulate_without_params(action=action, identification=identification)
        else:
            return server_manager.manipulate_with_params(action=action, identification=identification, **params)

    @staticmethod
    def delete_servers(user, identification=None):
        server_manager = server.ServerManager(user=user)
        return server_manager.delete(identification=identification)

    @staticmethod
    def create_flavor(user, params):
        flavor_manager = flavor.FlavorManager(user=user)
        return flavor_manager.create(**params)

    @staticmethod
    def show_flavor(user):
        flavor_manager = flavor.FlavorManager(user=user)
        return flavor_manager.get()

    @staticmethod
    def update_flavor(user, params):
        flavor_manager = flavor.FlavorManager(user=user)
        flavor_manager.delete(params["identification"])
        return flavor_manager.create(**params)

    @staticmethod
    def delete_flavor(user, identification):
        flavor_manager = flavor.FlavorManager(user=user)
        return flavor_manager.delete(identification)

    # TODO(dc): key pair action
    # @staticmethod
    # def create_keypair(user, ):
    #     pass
    #
    # @staticmethod
    # def show_keypair(user, ):
    #     pass
    #
    # @staticmethod
    # def delete_keypair(user, ):
    #     pass

    @staticmethod
    def check_action(user, ):
        if user.enable is False or user.flag == 'sys':
            return None
        else:
            return {
                "ACTIVE": [
                    {
                        "name": "snapshot",
                        "href": "/manipulateServer",
                    },
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "pause",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "suspend",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "shelve",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "resize",
                        "href": "/manipulateServer"
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "soft_reboot",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "hard_reboot",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "stop",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "rebuild",
                        "href": "/manipulateServer"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    },
                    {
                        "name": "live_migrate",  # admin
                        "href": "/manipulateServer"
                    },
                ],
                "PAUSED": [
                    {
                        "name": "snapshot",
                        "href": "/manipulateServer",
                    },
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "unpause",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "shelve",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    }
                ],
                "SUSPENDED": [
                    {
                        "name": "snapshot",
                        "href": "/manipulateServer",
                    },
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "unsuspend",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "shelve",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    }
                ],
                "SHUTOFF": [
                    {
                        "name": "snapshot",
                        "href": "/manipulateServer",
                    },
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "start",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "shelve",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    },
                    {
                        "name": "rebuild",
                        "href": "/manipulateServer"
                    },
                    {
                        "name": "resize",
                        "href": "/manipulateServer"
                    },
                    {
                        "name": "hard_reboot",
                        "href": "/manipulateServerNoParams"
                    }
                ],
                "VERIFY_RESIZE": [
                    {
                        "name": "confirm_resize",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "revert_resize",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    },
                    {
                        "name": "stop",
                        "href": "/manipulateServerNoParams"
                    }
                ],
                "SHELVED_OFFLOADED": [
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "unshelve",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    }
                ],
                "OTHER": [
                    {
                        "name": "update",
                        "href": "/updateServer",
                    },
                    {
                        "name": "lock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "unlock",
                        "href": "/manipulateServerNoParams"
                    },
                    {
                        "name": "delete",
                        "href": "/deleteServer"
                    }
                ]
            }
