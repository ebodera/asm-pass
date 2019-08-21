import os
# import api
from japronto import Application

#** Variables **#
web_port  = int(os.environ.get('PORT', 8000))

# config = [
#     # user api pages
#     ('/api/v1/user/', api.user.user_create, ['PUT']),
#     ('/api/v1/user/{user_id}', api.user.user_exists, ['GET']),
#     ('/api/v1/user/{user_id}', api.user.user_delete, ['DELETE']),
#     ('/api/v1/user/{user_id}/summary', api.user.user_summary, ['GET']),
#     ('/api/v1/user/{user_id}/summary', api.user.user_update, ['POST']),
#     # event api pages
#     ('/api/v1/event/', api.event.event_create, ['PUT']),
#     ('/api/v1/event/{event_id}', api.event.event_exists, ['GET']),
#     ('/api/v1/event/{event_id}', api.event.event_delete, ['DELETE']),
#     ('/api/v1/event/{event_id}/summary', api.event.event_summary, ['GET']),
#     ('/api/v1/event/{event_id}/summary', api.event.event_update, ['POST']),
# ]

#** Start **#

def hello(request):
    return request.Response(text='Hello world!')

app = Application()
# add routes w/ config
# for route in config:
#     app.router.add_route(route[0], route[1], methods=route[2])
# run app w/ given settings
app.router.add_route('/hello', hello)
app.run(port=web_port, debug=True)
