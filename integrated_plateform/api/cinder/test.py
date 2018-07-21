# # all return is JSON
import json

import keystone.client as keystoneclient
import client as cinderclient

# Get a user auth
kc = keystoneclient.Client()
key = 'dj+m~Fn_]DMk=EOSEk@CdcEYriIw~U_Q$x0d'
vdc_user = kc.register_user(key=key)

sys_user = kc.register_user(auth='system')

cc = cinderclient.Client()

volume_result = cc.show_volume(user=sys_user)
print(json.dumps(json.loads(volume_result), sort_keys=True, indent=4, separators=(',', ': ')))

