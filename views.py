'''
Created on 22/01/2014

@author: Capi
'''
import os

from google.appengine.api import users
from google.appengine.ext import webapp

import jinja2

JINJA_ENVIROMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp.RequestHandler):
    def get(self, name):

        template = JINJA_ENVIROMENT.get_template('index.html')
        self.response.out.write(template.render({}))


class ListDoctorsPage(webapp.RequestHandler):

    def get(self):

        user = users.get_current_user()

        if user:
            if users.is_current_user_admin():
                template = JINJA_ENVIROMENT.get_template('doctors_list.html')
                self.response.out.write(template.render({}))
            else:
                self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))





