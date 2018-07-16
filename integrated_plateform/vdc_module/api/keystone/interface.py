# coding=utf-8
import authentication
import project


def pwd_login(user):
    user = authentication.unscpoed(user)
    if user.token.unscoped_token_value is None:
        return None
    pjlist = project.show(user)
    user.project.pjlist = pjlist
    user.project.pjnum = len(user.project.pjlist)
    # when logging in, current pj is set as number 0, could change later
    user.project.currentpj = pjlist[0]
    user = authentication.scoped(user)
    return user
