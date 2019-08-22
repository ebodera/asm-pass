"""
api pages related to user/event connection data
"""
from . import utils
from . import log, db_conn, verify_otp

#** Functions **#

def user_list_events(req):
    """GET => list events connected to user-id"""
    user_id = req.match_dict['user_id']
    try:
        json = db_conn.user_list_events(user_id)
        json = {k.lower():v for k,v in json.items()}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def user_event_status(req):
    """GET => return status of specific requested event"""
    user_id  = req.match_dict['user_id']
    event_id = req.match_dict['event_id']
    try:
        json = db_conn.user_event_status(user_id, event_id)
        json = {k.lower():v for k,v in json.items()}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def user_checkin(req):
    """POST => attempt to checkin for the given event and user"""
    user_id  = req.match_dict['user_id']
    event_id = req.match_dict['event_id']
    try:
        utils.assert_keys(req.form, ['otp'])
        verify_otp(req.form['otp'])
        db_conn.user_checkin(user_id, event_id)
        json = {'checkin': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)
