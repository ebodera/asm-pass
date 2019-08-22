import os
import pyotp
import api.db
from datetime import datetime, timedelta

auth = (
    'root',
    os.environ['DB_PASS']
)
otp_base = os.environ['OTP_BASE']

totp = pyotp.TOTP(otp_base)
print('totp: %r' % totp.now())
raise SystemExit()

db   = api.db.Database(auth)

user_id = db.user_new(
    firstname='John',
    lastname='Doe',
    email='jdoe2@example.com',
)
event_id = db.event_new(
    creator_id=user_id,
    title='Sick Chilling Event',
    description='ready to sick chill? if you aint chillin, you a villan!',
    startdate=datetime.now() + timedelta(1),
    enddate=datetime.now() + timedelta(2)
)

# user modifiication

# get summary1
summary1 = db.user_summary(user_id)
print('user summary1: %s' % summary1)
# update the email
db.user_update(user_id, email='anonymous@exampe.com')
# retrieve new email
summary2 = db.user_summary(user_id)
print('user summary2: %s' % summary2)
# update the email back
db.user_update(user_id, email=summary1['Email'])

# event modifiication

# get summary1
summary1 = db.event_summary(event_id)
print('event summary: %s' % summary1)
# update the event
db.event_update(event_id, description='event is cancelled, sorry!')
# retrieve new data
summary2 = db.event_summary(event_id)
print('event summary2: %s' % summary2)
# update the summary back
db.event_update(event_id, description=summary1['Description'])

# show permissions for event
events = db.user_list_events(user_id)
print(events)

# delete everything

db.user_delete(user_id)
db.event_delete(event_id)
