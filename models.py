'''
Created on 22/01/2014

@author: Capi
'''
from google.appengine.ext import db


class Doctor(db.Model):
    full_name = db.StringProperty(required=True)
    specialities = db.StringProperty()
    email = db.EmailProperty(required=True)
    sent = db.BooleanProperty(default=False)
    want_test = db.BooleanProperty(default=False)
    poll_open = db.BooleanProperty(default=False)
    user = db.StringProperty()


