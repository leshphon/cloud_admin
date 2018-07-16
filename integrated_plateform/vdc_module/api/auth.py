# coding=utf-8
'''
Firstly, just define API.
Implementation is delayed util database is created.
'''
def check_url(user, url):
    '''
    user: who post the request with this url
    url: the url is currently request

    If the current user is authorized, just return ok
    '''
    return True;

def check_obj(user, obj, operation):
    '''
    user: who is to make specific operation on obj
    obj: the target of requested operation
    operation: what will operate on requested object

    if the user is authorized on requested operation,
    just return true.
    '''
    return True;
