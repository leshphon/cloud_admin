# API testing here

import client

# Get a client instance
cl = client.Client()

# get a project key and database contain it
# quota_data = {"gigabytes": 999, "backup_gigabytes": 999, "cores": 15, "instances": 25, "ram": 50000}
# key = cl.attach2project(quota_params=quota_data)

# register a vdc user and return is a user class from keystone api
vdc_user = cl.register_user(key=("DQvsrCWt8Ap_" + "11C4C=_NFpnO5Y4xU[" + "\\" + "\\" + "}Ku5"))

# register a system user and return is a user class from keystone api
system_user = cl.register_user(auth='system')

# # quota action get and update return is a quota class from keystone api
# quota = cl.get_quota(key=key, obj=vdc_user)
# print('volume: ' + str(quota.gigabytes), 'backup_volume: ' + str(quota.backup_gigabytes),
#       'cores: ' + str(quota.cores), 'instances: ' + str(quota.instances), 'ram: ' + str(quota.ram),)
#
# print('used_volume: ' + str(quota.usage.gigabytes), 'used_backup_volume: ' + str(quota.usage.backup_gigabytes),
#       'used_cores: ' + str(quota.usage.cores), 'used_instances: ' + str(quota.usage.instances), 'used_ram: ' +
#       str(quota.usage.ram))
#
# quota = cl.update_quota(key=key, obj=vdc_user, quota_params=
#                         {"gigabytes": 998, "backup_gigabytes": 997, "cores": 10, "instances": 23, "ram": 512000})
# print('volume: ' + str(quota.gigabytes), 'backup_volume: ' + str(quota.backup_gigabytes),
#       'cores: ' + str(quota.cores), 'instances: ' + str(quota.instances), 'ram: ' + str(quota.ram),)
#
# # revoke user
# cl.revoke_user(vdc_user)
# cl.revoke_user(system_user)
