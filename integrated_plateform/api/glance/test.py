# # all return is JSON
import json

import keystone.client as keystoneclient
import client as glanceclient

# Get a user auth
kc = keystoneclient.Client()
key = 'dj+m~Fn_]DMk=EOSEk@CdcEYriIw~U_Q$x0d'
vdc_user = kc.register_user(key=key)

# create and upload a image, this allow same name
gc = glanceclient.Client()
path = 'C:\Users\dc\Downloads\cirros-0.3.3-x86_64-disk.img'
params = {
        "container_format": "bare",
        "disk_format": "qcow2",
        "name": "test_up_c5",
        "min_disk": 10,
        "min_ram": 2048,
        "protected": False,
        "visibility": "public",
        "tags": ["create_user"]
    }
gc.create_image(user=vdc_user, upload_file=open(path, 'rb'), params=params)

# # show images
vdc_images = gc.show_image(user=vdc_user)
print(json.dumps(json.loads(vdc_images), sort_keys=True, indent=4, separators=(',', ': ')))

# update a images belong to vdc_user
update_result = gc.update_image(user=vdc_user, identification="8a235af0-2f2d-4466-aa97-35a2c04f15c4",
                                # another vdc's images will cause auth error "6bd87912-1df3-45a3-aaa9-bcbe30f62b28",
                                params={"name": "test_up_c2", "visibility": "public", "protected": False})
print(json.dumps(json.loads(update_result), sort_keys=True, indent=4, separators=(',', ': ')))

# delete a images belong to vdc_user
gc.delete_image(user=vdc_user, identification="8a235af0-2f2d-4466-aa97-35a2c04f15c4")
print(json.dumps(json.loads(update_result), sort_keys=True, indent=4, separators=(',', ': ')))

# TODO(dc): django view(how to create a image)
# def upload_test(request):
#     if request.method == "POST":
#         unscoped_user = User(username='admin', password='admin', domain=Domain(current_domain="Default"))
#         scoped_user = keystoneclient.pwd_login(unscoped_user)
#         url = 'http://10.141.209.213:9292/v2/'
#         headers = {
#             'X-Auth-Token': scoped_user.token.scoped_token_value,
#             "Content-type": "application/octet-stream"
#         }
#         temp_file = request.FILES.get("file", None)
#         if not temp_file:
#             return HttpResponse("no files for upload!")
#         # with open('/tmp/' + temp_file.name, 'wb+') as destination:
#         #     for chunk in temp_file.chunks():
#         #         destination.write(chunk)
#         result = requests.put(url=url + '/images/' + "6bd87912-1df3-45a3-aaa9-bcbe30f62b28" + '/file', data=None,
#                               headers=headers, files=temp_file.file)
#         temp_file.close()
#         print("finished")
#         return HttpResponse("upload over!")
#     else:
#         return render(request, 'vdc_module/test.html')
