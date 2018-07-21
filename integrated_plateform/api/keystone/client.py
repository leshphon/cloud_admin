# coding=utf-8
import warnings

import project
import user
import role
import quota
import utils


class Client(object):

    def __init__(self):
        self.client_name = 'Keystone'

    @staticmethod
    def register_user(key=None,
                      auth='vdc'):  # TODO(dc): domain is not concerned and set to default
        """

        :param key: openstack project key that database contain
        :param auth: access openstack model and value  is 'system' and 'vdc'
        :return: class user that will be used in other api
        """
        project_manager = project.ProjectManger()
        user_manager = user.UserManager()

        if auth == 'system' and key is None:
            return user_manager.get(name=utils.init_data().get('host', 'ADMIN'),
                                    passwd=utils.init_data().get('host', 'PASSWD'),
                                    project=project_manager.get(name=utils.init_data().get('host', 'PROJECT')),
                                    domain=utils.init_data().get('host', 'DOMAIN'),
                                    flag='sys')
        elif auth == 'vdc':
            if key is None:
                warnings.warn("Wrong param key!")
                return None
            if isinstance(key, str) is False:
                warnings.warn("Wrong param key!")
                return None
            return user_manager.get(project=project_manager.get(key[0:(len(key) / 3)]),
                                    name=key[(len(key) / 3):(2 * len(key) / 3)],
                                    passwd=key[(2 * len(key) / 3):],
                                    domain=utils.init_data().get('host', 'DOMAIN'))

        else:
            warnings.warn("Register_user wrong auth parameters!")

    @staticmethod
    def revoke_user(obj):
        """

        :param obj: a class user from keystone api
        :return: None
        """
        utils.revoke_obj(obj)

    @staticmethod
    def attach2project(quota_params=None):
        """

        :param quota_params: a dict quota data just like
                            {"gigabytes": 999, "backup_gigabytes": 999, "cores": 15, "instances": 25, "ram": 50000}
        :return: openstack project key that database will contain
        """
        project_manager = project.ProjectManger()
        user_manager = user.UserManager()
        role_manager = role.RoleManager()
        quota_manager = quota.QuotaManager()

        my_project = project_manager.create(name=utils.rstr_gen(12))
        my_user = user_manager.create(project=my_project, name=utils.rstr_gen(12), passwd=utils.rstr_gen(12),
                                      role=role_manager.get("admin"))

        # TODO(dc): not concerned volume num, volume snapshot num, float-ip num, key_pairs
        quota_params["volumes"] = -1
        quota_params["snapshots"] = -1

        quota_params["floating_ips"] = -1
        quota_params["key_pairs"] = -1

        quota_manager.update(project=my_project, user=my_user, **quota_params)

        utils.revoke_obj(project_manager)
        utils.revoke_obj(user_manager)
        utils.revoke_obj(role_manager)
        utils.revoke_obj(quota_manager)

        return my_project.name + '' + my_user.name + '' + my_user.passwd

    def update_quota(self, key, obj, quota_params=None):
        """

        :param key: openstack project key that database contain
        :param obj: a class user from keystone api
        :param quota_params: a dict quota data just like ans this could not be full
                            {"gigabytes": 999, "backup_gigabytes": 999, "cores": 15, "instances": 25, "ram": 50000}
        :return: a class quota from keystone api
        """
        project_manager = project.ProjectManger()
        quota_manager = quota.QuotaManager()

        my_project = project_manager.get(key[0:(len(key) / 3)])
        if obj.flag != 'sys':
            if obj.project.identification != my_project.identification:
                print("This user has no auth to access the key's project")
                return None
        my_quota = quota_manager.update(project=my_project, user=obj, **quota_params)

        utils.revoke_obj(project_manager)
        utils.revoke_obj(quota_manager)
        return my_quota

    def get_quota(self, key, obj):
        """

        :param key: openstack project key that database contain
        :param obj: a class user from keystone api
        :return: a class quota from keystone api
        """
        project_manager = project.ProjectManger()
        quota_manager = quota.QuotaManager()

        my_project = project_manager.get(key[0:(len(key) / 3)])
        if obj.flag != 'sys':
            if obj.project.identification != my_project.identification:
                print("This user has no auth to access the key's project")
                return None
        my_quota = quota_manager.get(project=my_project, user=obj)

        utils.revoke_obj(project_manager)
        utils.revoke_obj(quota_manager)
        return my_quota

    # def show_vdc(self):
    #     """
    #     """
        # TODO not concerned now
