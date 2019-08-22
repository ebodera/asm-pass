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
        json = [{k.lower():v for k,v in item.items()} for item in json]
        json = {'results': json}
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

def user_list_event_summary(req):
    """GET => list events tied to a user and the summary info for each"""
    user_id = req.match_dict['user_id']
    try:
        json1 = db_conn.user_list_events(user_id)
        json1 = [{k.lower():str(v) for k,v in item.items()} for item in json1]
        for result in json1:
            event_id = result['eventid']
            json2    = db_conn.event_summary(event_id)
            arrived  = db_conn.count_event_users(event_id, arrived=True)
            json2['arrived'] = arrived['COUNT(UserID)']
            result.update({k.lower():str(v) for k,v in json2.items()})
        json = {'results': json1}
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
