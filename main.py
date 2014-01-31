
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import views


urls = [
        ('/', views.MainPage),
        ('/amministratore', views.ListDoctorsPage),
        ('/(\w+)', views.MainPage),
        ]


application = webapp.WSGIApplication(urls, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
