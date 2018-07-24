import json

import keystone.client as keystoneclient
import client as novaclient

# Get a user auth
kc = keystoneclient.Client()
key = ('dj+m~Fn_]DMk' + '=EOSEk@CdcEY' + 'riIw~U_Q$x0d')
vdc_user = kc.register_user(key=key)
sys_user = kc.register_user(auth='system')

nc = novaclient.Client()
# FLAVOR
# show flavor
# show_flavor = nc.show_flavor(user=sys_user)
# print(json.loads(show_flavor)["flavors"][0]["id"])

# INSTANCE
# create instance
ci_params = {
    "owner": "user1",
    "name": "api-test1",
    "flavorRef": "f841e83f-9ec0-4f1f-a1ca-a0518b9f1939",
    # "net_uuid": "ef4063ea-27cc-487f-b574-51652f8a48e0",
    "port_id": "36d94576-16bd-4948-a0fc-afea687ccc66",
    "source_type": "image",
    "destination_type": "volume",
    "volume_size": 2,
    "source_uuid": "de19ca79-705e-4865-b7f5-96ecb3c96460",
    "delete_on_termination": True
    }
create_instance = nc.create_servers(user=sys_user, params=ci_params)
pass

# update_instance = nc.update_servers(user=sys_user, params={"name": "api-test2"},
#                                     identification="147508b2-e63e-4e27-94b6-4c1e80fa2867")
# print(json.dumps(json.loads(update_instance), sort_keys=True, indent=4, separators=(',', ': ')))

# de_re = nc.delete_servers(user=sys_user, identification="1d15bf9e-ae61-4ab9-a35d-7d8077f5c35b")
# print(json.dumps(json.loads(de_re), sort_keys=True, indent=4, separators=(',', ': ')))
show_instance = nc.show_servers(user=sys_user)
pass