# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from vdc_module.api.member import User, Token, Domain
import vdc_module.api.keystone.interface as keystoneclient
import vdc_module.api.nova.interface as novaclient
import vdc_module.api.neutron.interface as neutronclient
import vdc_module.api.glance.interface as glanceclient
import json


# Create your views here.
def vdc_index(request):
    return render(request, 'vdc_module/vdc_index.html', {
        'error': 'here is error message',
    })


def instance_manage(request):
    openstack_login(request)
    user = request.session.get('user')
    return render(request, 'vdc_module/vdc_instance_manage.html', {
        'currentpj': user.project.currentpj,
        'current_role_name': user.role.current_role_name
    })


def instance_create(request):
    return render(request, 'vdc_module/vdc_create_instance.html')


def create_server(request):
    user = request.session.get("user")
    info = request.POST.get("data_body")
    # info = request.body
    # print(info)
    # print(info)
    result = novaclient.server.create(user, info)
    return HttpResponse(result)


def openstack_login(request):
    unscoped_user = User(username='admin', password='admin', domain=Domain(current_domain="Default"))
    scoped_user = keystoneclient.pwd_login(unscoped_user)
    print scoped_user.token
    print('login')
    if scoped_user is None:
        return HttpResponse('用户名或密码错误')
    # Set session
    request.session['user'] = scoped_user


def show_server(request):
    result = novaclient.server.show(user=request.session.get("user"))
    return HttpResponse(result, content_type="application/json")


def showNet(request):
    result = neutronclient.networks.show(user=request.session.get("user"))
    return HttpResponse(result, content_type="application/json")


def show_flavors(request):
    result = novaclient.flavor.show(user=request.session.get("user"), flavor_id=None)
    return HttpResponse(result, content_type="application/json")


def show_image(request):
    result = glanceclient.image.show(user=request.session.get("user"), image_id=None, value=None)
    return HttpResponse(result, content_type="application/json")


def show_keypairs(request):
    result = novaclient.keypairs.show(user=request.session.get("user"))
    return HttpResponse(result, content_type="application/json")


def getStatusAction(request):
    return HttpResponse(
        json.dumps(novaclient.server.status.checkAction(user=request.session.get("user"))),
        content_type="application/json"
    )


def pauseServer(request):
    result = novaclient.server.pause(user=request.session.get("user"), server_id=request.POST.get('server_id'))
    return HttpResponse(result, content_type="application/json")


def unpauseServer(request):
    item_id = request.POST.get('server_id')
    result = novaclient.server.unpause(user=request.session.get("user"), server_id=item_id)
    return HttpResponse(result, content_type="application/json")


def suspendServer(request):
    # if request.is_ajax() and request.method == 'POST':
    result = novaclient.server.suspend(user=request.session.get("user"), server_id=request.POST.get('server_id'))
    return HttpResponse(result, content_type="application/json")


def unsuspendServer(request):
    # if request.is_ajax() and request.method == 'POST':
    result = novaclient.server.unsuspend(user=request.session.get("user"), server_id=request.POST.get('server_id'))
    return HttpResponse(result, content_type="application/json")


def deleteServer(request):
    # if request.is_ajax() and request.method == 'POST':
    server_id = request.POST.get('server_id')
    result = novaclient.server.delete(user=request.session.get("user"), server_id=server_id)
    # return HttpResponse(result, content_type="application/json")
    return HttpResponse(result)


def showSingleSever(request):
    item_id = request.POST.get('server_id')
    result = novaclient.server.details(user=request.session.get("user"), server_id=item_id)
    return HttpResponse(result, content_type="application/json")
