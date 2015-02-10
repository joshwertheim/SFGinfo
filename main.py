import os
import urllib
import json

import jinja2
import webapp2

from google.appengine.ext import db
from google.appengine.api import urlfetch

from feed import Feed
from newsstory import NewsStory
from player import Player
from player import Roster

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Testrr(object):
    check = False

class RosterPage(webapp2.RequestHandler):
    """docstring for RosterPage"""
    def get(self):
        r = Roster()
        if not Testrr.check:    
            r.prepare_players()
            Testrr.check = True
        q = Player.all()
        q.order('first_last')
        players = q.fetch(limit=62)

        template_values = {
            'players': players,
        }

        template = JINJA_ENVIRONMENT.get_template('templates/roster.html')
        self.response.write(template.render(template_values))

class NewsPage(webapp2.RequestHandler):
    def get(self):
        message = "Latest Giants Headlines"

        headlines_url = "http://sanfrancisco.giants.mlb.com/gen/sf/news/headlines.json"
            
        feed = Feed(headlines_url)
        feed.load_and_prepare()
        succeeded, loaded_headlines_json = feed.get_representation
        length = len(loaded_headlines_json["members"])

        members = loaded_headlines_json["members"]
        stories = list()

        for entry in members:
            try:
                althead = entry["althead"]
                blurb = entry["blurb"]
                story_url = entry["url"]
                article = NewsStory(althead, blurb, story_url)

                stories.append(article)
            except KeyError, e:
                print 'KeyError - reason "%s"' % str(e)

        template_values = {
            'message': message,
            'stories': stories,
        }

        template = JINJA_ENVIRONMENT.get_template('templates/news.html')
        self.response.write(template.render(template_values))

class LandingPage(webapp2.RequestHandler):
    """docstring for LandingPage"""
    
    def get(self):
        news_info = "/news"
        roster_info = "/roster"

        template_values = {
            'news_url': news_info,
            'roster_url': roster_info,
        }
        
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))

# class PlayerPage(webapp2.RequestHandler):
#     """docstring for PlayerPage"""
    
#     def get():
        
        
        

application = webapp2.WSGIApplication([
    ('/', LandingPage),
    ('/news', NewsPage),
    ('/roster', RosterPage),
], debug=True)