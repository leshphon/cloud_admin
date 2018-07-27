# coding=utf-8

import server
import flavor


class Client(object):
    def __init__(self):
        self.client_name = 'Nova'

    @staticmethod
    def create_servers(user, params):
        server_manager = server.ServerManager(user=user)
        flavor_manager = flavor.FlavorManager(user=user)
        result = server_manager.create(**params)
        if isinstance(result, list):
            result[0].flavor_obj = flavor_manager.get(identification=result[0].flavor_id)
            return result
        else:
            return result

    @staticmethod
    def show_servers(user, owner=None, identification=None):
        server_manager = server.ServerManager(user=user)
        return server_manager.get(owner=owner, identification=identification)

    @staticmethod
    def update_servers(user, params, identification):
        server_manager = server.ServerManager(user=user)
        return server_manager.update(identification, **params)

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
        params = {"project_id": user.project.identification}
        return flavor_manager.get(**params)

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
        # if user.enable is False or user.flag == 'sys':
        #     return None
        # else:
            return {
                "ACTIVE": [
                    {
                        "cn_name": "创建快照存为镜像",
                        "name": "snapshot",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "暂停实例",
                        "name": "pause",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "挂起实例",
                        "name": "suspend",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "废弃实例",
                        "name": "shelve",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "调整实例大小",
                        "name": "resize",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "软重启实例",
                        "name": "soft_reboot",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "硬重启实例",
                        "name": "hard_reboot",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "关闭实例",
                        "name": "stop",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "重建实例",
                        "name": "rebuild",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "迁移实例",
                        "name": "live_migrate",  # admin
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_admin"
                    },
                ],
                "PAUSED": [
                    {
                        "cn_name": "创建快照存为镜像",
                        "name": "snapshot",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "恢复实例",
                        "name": "unpause",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "废弃实例",
                        "name": "shelve",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    }
                ],
                "SUSPENDED": [
                    {
                        "cn_name": "创建快照存为镜像",
                        "name": "snapshot",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "恢复实例",
                        "name": "unsuspend",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "废弃实例",
                        "name": "shelve",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    }
                ],
                "SHUTOFF": [
                    {
                        "cn_name": "创建快照存为镜像",
                        "name": "snapshot",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "开启实例",
                        "name": "start",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "废弃实例",
                        "name": "shelve",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "重建实例",
                        "name": "rebuild",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "调整实例大小",
                        "name": "resize",
                        "href": "/vdc_manipulateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "硬重启实例",
                        "name": "hard_reboot",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    }
                ],
                "VERIFY_RESIZE": [
                    {
                        "cn_name": "确认实例大小调整",
                        "name": "confirm_resize",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "取消实例大小调整",
                        "name": "revert_resize",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "关闭实例",
                        "name": "stop",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    }
                ],
                "SHELVED_OFFLOADED": [
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "取消废弃实例",
                        "name": "unshelve",
                        "href": "/vdc_manipulateServerNoParams",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    }
                ],
                "OTHER": [
                    {
                        "cn_name": "更新实例",
                        "name": "update",
                        "href": "/vdc_updateServer",
                        "role": "vdc_user"
                    },
                    {
                        "cn_name": "删除实例",
                        "name": "delete",
                        "href": "/vdc_deleteServer",
                        "role": "vdc_user"
                    }
                ]
            }
