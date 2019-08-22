"""
api pages related to user functions
"""
from . import log, db_conn
from . import utils

#** Variables **#
_user_args = ['firstname', 'lastname', 'email']

#** Functions **#

def user_create(req):
    """PUT => create a user account or error"""
    try:
        utils.assert_keys(req.form, _user_args)
        user_id = db_conn.user_new(**req.form)
        json = {'user_id': user_id}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def user_exists(req):
    """GET => return true/false if user exists"""
    user_id = req.match_dict['user_id']
    try:
        db_conn.user_exists(user_id)
        json = {'exists': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def user_delete(req):
    """DELETE => delete a user account or error"""
    user_id = req.match_dict['user_id']
    try:
        db_conn.user_delete(user_id)
        json = {'deleted': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def user_summary(req):
    """GET => collect summary of user or error"""
    user_id = req.match_dict['user_id']
    try:
        json = db_conn.user_summary(user_id)
        json = {k.lower():v for k,v in json.items()}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def user_update(req):
    """POST => update values for specific fields as given"""
    user_id = req.match_dict['user_id']
    try:
        data = utils.find_keys(req.form, _user_args)
        db_conn.user_update(**data)
        json = {'updated': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)
