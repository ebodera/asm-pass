"""
api pages related to events
"""
from . import log, db_conn
from . import utils

#** Variables **#
_event_args = ['title', 'description', 'start_date', 'end_date']

#** Functions **#

def event_create(req):
    """PUT => create a event account or error"""
    try:
        utils.assert_keys(req.form, ['creator_id']+_event_args)
        event_id = db_conn.event_new(**req.form)
        json = {'event_id': event_id}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def event_exists(req):
    """GET => return true/false if event exists"""
    event_id = req.match_dict['event_id']
    try:
        db_conn.event_exists(event_id)
        json = {'exists': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def event_delete(req):
    """DELETE => delete an event or error"""
    event_id = req.match_dict['event_id']
    try:
        db_conn.event_delete(event_id)
        json = {'deleted': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def event_summary(req):
    """GET => collect summary of event or error"""
    event_id = req.match_dict['event_id']
    try:
        json = db_conn.event_summary(event_id)
        json = {k.lower():v for k,v in json.items()}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)

def event_update(req):
    """POST => update values for specific fields as given"""
    event_id = req.match_dict['event_id']
    try:
        data = utils.find_keys(req.form, _event_args)
        db_conn.event_update(**data)
        json = {'updated': True}
    except Exception as e:
        json = {'errors': [str(e)]}
    return req.Response(json=json)
