# coding=utf-8
from django.shortcuts import redirect
import vdc_module.api.keystone.interface as keystoneclient
from vdc_module.api.member import User


# Token identify with decoration
def auth(func):
    def inner(request, *args, **kwargs):
        user = request.session.get("user")
        # 没有user的cookie
        if not user:
            return redirect("login")
        # 有user的cookie
        user = keystoneclient.authentication.check(user)
        # 判断user的token是否过期
        if user.enabled is False:
            return redirect("login")
        return func(request, *args, **kwargs)
    return inner


# def set_session_from_user(request, user):
#     request.session['token'] = user.token
#     request.session['user_id'] = user.id
#     request.session['region_endpoint'] = user.endpoint
#     request.session['user_name'] = user.username
#     request.session['user_id'] = user.id
#     request.session['pjname'] = user.project_name
#     request.session['pjlist'] = user.project_list
#     request.session['role_name'] = user.roles
#     # Update the user object cached in the request
#     # request._cached_user = user
#     # request.user = user


# def get_info_from_session(request):
#     token = request.session.get('token')
#     region_endpoint = request.session.get('region_endpoint')
#     user_name = request.session.get('user_name')
#     user_id = request.session.get('user_id')
#     project_name = request.session.get('pjname')
#     project_list = request.session.get('pjlist')
#     roles = request.session.get('role_name')
#     info = User(user=user_name, id=user_id, token=token, domain_name=None, pjname=project_name, pjlist=project_list,
#                 roles=roles, unscoped_token=None, password=None, endpoint=region_endpoint, enabled=True)
#     return info
