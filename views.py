'''
Created on 22/01/2014

@author: Capi
'''
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):
    def get(self):

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')

        self.response.out.write(template.render(path, {}))


class ListDoctorsPage(webapp.RequestHandler):

    ADMIN_EMAIL = 'cpinelly@gmail.com'

    def get(self):

        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                path = os.path.join(os.path.dirname(__file__), 'templates/doctors_list.html')
                self.response.out.write(template.render(path, {}))
            else:
                self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))




