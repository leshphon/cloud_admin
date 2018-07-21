# coding=utf-8
import requests
import json
import warnings


class QuotaManager(object):
    """

    """

    def __init__(self):
        self.enable = True
        self.token = None

    def update(self, project=None, user=None, **kwargs):
        quota_url = user.endpoint['nova'] + '/os-quota-sets' + '/' + project.identification
        volume_quota_url = (user.endpoint['cinder'] + '/' + user.project.identification + '/os-quota-sets/' +
                            project.identification)

        # TODO(dc): update user quota is not concerned
        # if user is not None:
        #     quota_url = quota_url + '?user_id=' + user.identification
        #     volume_quota_url = volume_quota_url + '?user_id=' + user.identification

        quota_params = {
            "quota_set": {
            }
        }
        quota_flag = False

        volume_quota_params = {
            "quota_set": {
            }
        }
        volume_quota_flag = False

        if project is None:
            warnings.warn("Update project without project obj")
            return None

        if kwargs.get("cores"):
            quota_params["quota_set"]["cores"] = kwargs.get("cores")
            quota_flag = True
        if kwargs.get("instances"):
            quota_params["quota_set"]["instances"] = kwargs.get("instances")
            quota_flag = True
        if kwargs.get("ram"):
            quota_params["quota_set"]["ram"] = kwargs.get("ram")
            quota_flag = True
        if kwargs.get("floating_ips"):
            quota_params["quota_set"]["floating_ips"] = kwargs.get("floating_ips")
            quota_flag = True
        if kwargs.get("key_pairs"):
            quota_params["quota_set"]["key_pairs"] = kwargs.get("key_pairs")
            quota_flag = True

        if kwargs.get("gigabytes"):
            volume_quota_params["quota_set"]["gigabytes"] = kwargs.get("gigabytes")
            volume_quota_flag = True
        if kwargs.get("backup_gigabytes"):
            volume_quota_params["quota_set"]["backup_gigabytes"] = kwargs.get("backup_gigabytes")
            volume_quota_flag = True
        if kwargs.get("volumes"):
            volume_quota_params["quota_set"]["volumes"] = kwargs.get("volumes")
            volume_quota_flag = True
        if kwargs.get("snapshots"):
            volume_quota_params["quota_set"]["snapshots"] = kwargs.get("snapshots")
            volume_quota_flag = True

        if quota_flag is True:
            requests.put(url=quota_url, data=json.dumps(quota_params), headers=user.headers)

        if volume_quota_flag is True:
            requests.put(url=volume_quota_url, data=json.dumps(volume_quota_params), headers=user.headers)
        return self.get(project=project, user=user)

    def get(self, user=None, project=None):
        quota_url = user.endpoint['nova'] + '/os-quota-sets' + '/' + project.identification
        volume_quota_url = (user.endpoint['cinder'] + '/' + user.project.identification + '/os-quota-sets/' +
                            project.identification)

        # TODO(dc): get user quota is not concerned
        # if user is not None:
        #     quota_url = quota_url + '?user_id=' + user.identification
        #     volume_quota_url = volume_quota_url + '?user_id=' + user.identification

        quota_result = requests.get(url=quota_url, headers=user.headers)
        dict_quota_result = json.loads(quota_result.content)

        volume_quota_result = requests.get(url=volume_quota_url, headers=user.headers)
        dict_volume_quota_result = json.loads(volume_quota_result.content)

        return Quota(cores=dict_quota_result["quota_set"]["cores"],
                     instances=dict_quota_result["quota_set"]["instances"],
                     gigabytes=dict_volume_quota_result["quota_set"]["gigabytes"],
                     backup_gigabytes=dict_volume_quota_result["quota_set"]["gigabytes"],
                     ram=dict_quota_result["quota_set"]["ram"],
                     usage=self.find_usage(project=project, user=user))

    def find_usage(self, project=None, user=None):
        usage_url = user.endpoint['nova'] + '/os-quota-sets' + '/' + project.identification
        volume_usage_url = (user.endpoint['cinder'] + '/' + user.project.identification + '/os-quota-sets/' +
                            project.identification) + '?usage=True'
        # TODO(dc): get user quota is not concerned
        # if user is not None:
        #     usage_url = usage_url + '?user_id=' + user.identification
        #     volume_usage_url = volume_usage_url + '&user_id=' + user.identification
        usage_url = usage_url + '/detail'

        usage_result = requests.get(url=usage_url, headers=user.headers)
        dict_usage_result = json.loads(usage_result.content)

        volume_usage_result = requests.get(url=volume_usage_url, headers=user.headers)
        dict_volume_usage_result = json.loads(volume_usage_result.content)

        return Usage(cores=dict_usage_result["quota_set"]["cores"]["in_use"],
                     instances=dict_usage_result["quota_set"]["instances"]["in_use"],
                     gigabytes=dict_volume_usage_result["quota_set"]["gigabytes"]["in_use"],
                     backup_gigabytes=dict_volume_usage_result["quota_set"]["backup_gigabytes"]["in_use"],
                     ram=dict_usage_result["quota_set"]["ram"]["in_use"])


class Quota(object):
    def __init__(self, cores, instances, gigabytes, backup_gigabytes, ram, usage):
        self.cores = cores
        self.instances = instances
        self.gigabytes = gigabytes
        self.backup_gigabytes = backup_gigabytes
        self.ram = ram
        self.usage = usage


class Usage(object):
    def __init__(self, cores, instances, gigabytes, backup_gigabytes, ram):
        self.cores = cores
        self.instances = instances
        self.gigabytes = gigabytes
        self.backup_gigabytes = backup_gigabytes
        self.ram = ram
