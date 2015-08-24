import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import urllib
import logging
import json



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Thesis(ndb.Model):
	thesis_year = ndb.StringProperty(indexed=True)
	thesis_title = ndb.StringProperty(indexed=True)
	thesis_abstract = ndb.StringProperty(indexed=True)
	thesis_adviser = ndb.StringProperty(indexed=True)
	thesis_section = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
    	user = users.get_current_user()

    	if user:
    		url = users.create_logout_url(self.request.uri)
    		url_linktext = 'Logout'

    		template_values = {
    			'user': user,
    			'url': url,
    			'url_linktext': url_linktext
    		}

    		template = JINJA_ENVIRONMENT.get_template('main.html')
    		self.response.write(template.render(template_values))
    	else:
    		self.redirect(users.create_login_url(self.request.uri))   

class APIThesis(webapp2.RequestHandler):
	def get(self):
		thesis = Thesis.query().order(-Thesis.date).fetch()
		thesis_list = []

		for entry in thesis:
			thesis_list.append({
				'id': entry.key.urlsafe(),
				'thesis_year': entry.thesis_year,
				'thesis_title': entry.thesis_title,
				'thesis_abstract': entry.thesis_abstract,
				'thesis_adviser': entry.thesis_adviser,
				'thesis_section': entry.thesis_section
			})

		response = {
        	'result': 'OK',
        	'data': thesis_list
        }

	        self.response.headers['Content-Type'] = 'application/json'
	        self.response.out.write(json.dumps(response))

	def post(self):
		thesis = Thesis()
		thesis.thesis_year = self.request.get('thesis_year')
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.thesis_abstract = self.request.get('thesis_abstract')
		thesis.thesis_adviser = self.request.get('thesis_adviser')
		thesis.thesis_section = self.request.get('thesis_section')
		thesis.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
		    'result': 'OK',
		        'data': {
		            'id': thesis.key.urlsafe(),
		            'thesis_year': thesis.thesis_year,
		            'thesis_title': thesis.thesis_title,
		            'thesis_abstract': thesis.thesis_abstract,
		            'thesis_adviser': thesis.thesis_adviser,
		            'thesis_section': thesis.thesis_section
		        }
		}
		self.response.out.write(json.dumps(response))

# class LogInPage(webapp2.RequestHandler):
# 	def get(self):
# 		template = JINJA_ENVIRONMENT.get_template('main.html')
# 		self.response.write(template.render())

# 		user = users.get_current_user()

# 		if user:
# 			self.response.headers['Content-Type'] = 'text/html; charset = utf - 8'
# 			self.response.write('Hello, ' + user.nickname())
# 		else:
# 			self.redirect('/')

app = webapp2.WSGIApplication([
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/api/thesis', APIThesis)
], debug=True)