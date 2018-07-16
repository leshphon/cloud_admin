# coding=utf-8
class Token(object):
    def __init__(self, unscoped_token_value=None, unscoped_token_id=None, scoped_token_value=None,
                 scoped_token_id=None):
        self.unscoped_token_value = unscoped_token_value
        self.unscoped_token_id = unscoped_token_id
        self.scoped_token_value = scoped_token_value
        self.scoped_token_id = scoped_token_id


class Role(object):
    def __init__(self, role_list=None, current_role_name=None, current_role_id=None):
        self.role_list = role_list
        self.current_role_name = current_role_name
        self.current_role_id = current_role_id


class Project(object):
    def __init__(self, pjlist={}, pjnum=None, currntpj=None):
        self.pjlist = pjlist
        self.pjnum = pjnum
        self.currentpj = currntpj


class Domain(object):
    def __init__(self, domains=None, current_domain=None):
        self.domains = domains
        self.current_domain = current_domain


class User(object):
    def __init__(self, username=None, userid=None, token=Token(), domain=Domain(), project=Project(), role=Role(),
                 password=None, endpoint=None, enabled=True):
        self.token = token
        self.user_id = userid
        self.username = username
        self.domain = domain
        self.project = project
        self.role = role
        self.password = password
        self.endpoint = endpoint
        self.enabled = enabled

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.username)

    def is_active(self):
        return self.enabled
