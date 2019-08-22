import os
import sys
import pyotp
import logging
from . import db

#** Variables **#

#TODO: there is no security or session
# management for any of these api-calls
# if this were to leave POC, there would
# be typical session token connection
# and permission control so that apps/
# app-spoofers could not access records
# they did not have access to

#TODO: this otp thing is literally worthless
# with a static base-secret that is included
# on all apps, later if this were to not be a POC
# the database would hold each starting secret
# to increase the security, that would be generated
# on creation of the user-account

otp_base = os.environ['OTP_BASE']
totp     = pyotp.TOTP(otp_base)

#** Functions **#

def _get_loglevel(level):
    """convert string log-level into logging constant"""
    try:
        return getattr(logging, level.upper())
    except:
        return logging.INFO

def make_logger(name, level):
    """
    spawn logging instance logging to stderr w/ appsec jsom formatter

    :param name:   name of the logging instance
    :param level:  level of the logging verbosity
    :param kwargs: arguments passed to the json-formatter
    :return:
        logging instance w/ given settings
    """
    # create log w/ debug log-level so level defintion is by handler
    log = logging.getLogger(name)
    log.propagate = 0
    log.setLevel(logging.DEBUG)
    # ensure that previus handlers are removed
    while log.handlers:
        log.handlers.pop()
    # add stream handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(_get_loglevel(level))
    # add formater to stream-handler
    formatter = logging.Formatter(_dfault_fmt)
    ch.setFormatter(formatter)
    # add stream-handler to log
    log.addHandler(ch)
    return log

def verify_otp(otp_str):
    """
    verify otp-string and return true if valid

    :param otp_str: otp string connected w/ otp
    """
    if not totp.verify(otp_str, valid_window=2):
        raise Exception('otp failed to verify')

#** Variables **#
_dfault_fmt = '%(asctime)s - %(name)s - %(levelname)-8s %(message)s'

log     = make_logger('api', 'debug')
db_conn = db.Database(host='us-cdbr-iron-east-02.cleardb.net', auth=(
    'b56635ab405c6c',
    '17574702',
), db='heroku_77b3479c73262cb')

# components
from . import user
from . import event
from . import user_event
