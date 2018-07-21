# # all return is JSON
import json

import keystone.client as keystoneclient
import client as neutronclient

# Get a user auth
kc = keystoneclient.Client()
key = 'dj+m~Fn_]DMk=EOSEk@CdcEYriIw~U_Q$x0d'
vdc_user = kc.register_user(key=key)

sys_user = kc.register_user(auth='system')

nc = neutronclient.Client()
