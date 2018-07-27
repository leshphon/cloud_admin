# # all return is JSON
import json

import api.keystone.client as keystoneclient
import client as neutronclient

# Get a user auth
kc = keystoneclient.Client()
key = ('dj+m~Fn_]DMk' + '=EOSEk@CdcEY' + 'riIw~U_Q$x0d')
vdc_user = kc.register_user(key=key)
sys_user = kc.register_user(auth='system')

nc = neutronclient.Client()
# NETWORK
# create network
# <provider:network_type> value: flat, vlan, vxlan, or gre
# <provider:physical_network>: The physical network where this network should be implemented
# <project_id>
# <shared>: True or False
# params = {"name": "net1", #"provider:network_type";, "provider:physical_network":,
#           "shared": False, "description": "test"} # "provider:physical_network": }
# cr_result = nc.create_network(user=vdc_user, params=params)

# update network
# up_result = nc.update_network(user=sys_user, identification='a659ce8a-9163-4a5e-8d8a-1df40c3bf863',
#                               params={'name': 'out', 'shared': True})

# show network
net_result = nc.get_network(user=sys_user)
print(json.dumps(json.loads(net_result), sort_keys=True, indent=4, separators=(',', ': ')))

# SUBNET
# sub_result = nc.get_subnet(user=sys_user, params={"network_id": "a659ce8a-9163-4a5e-8d8a-1df40c3bf863"})
# print(json.dumps(json.loads(sub_result), sort_keys=True, indent=4, separators=(',', ': ')))

# PORT
# port_result = nc.get_port(user=sys_user, params={"network_id": "ef4063ea-27cc-487f-b574-51652f8a48e0"})
# print(json.dumps(json.loads(port_result), sort_keys=True, indent=4, separators=(',', ': ')))

# cport_result = nc.create_port(user=sys_user,
#                               params={"network_id": "ef4063ea-27cc-487f-b574-51652f8a48e0",
#                                          "subnet_id": "dcda03cf-25f0-4a70-a938-fdab8fae12a4"})
# print(json.dumps(json.loads(cport_result), sort_keys=True, indent=4, separators=(',', ': ')))