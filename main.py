import os
import time
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

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

def getplayers():
    r = Roster()
    r.prepare_players()
    q = Player.all()
    q.order('first_last')
    size = q.count()
    players = q.fetch(limit=size)
    return players


class RosterPage(webapp2.RequestHandler):
    """docstring for RosterPage"""
    def get(self):
        r = Roster()
        q = Player.all()
        q.order('first_last')
        size = q.count()
        players = q.fetch(limit=size)

        if not players:
            players = getplayers()

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

class CacheCronPage(webapp2.RequestHandler):
    """docstring for CacheCronPage"""

    def get(self):
        q = Player.all()
        size = q.count()
        players = q.fetch(limit=size)
        db.delete(players)
        time.sleep(3)
        getplayers()

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

application = webapp2.WSGIApplication([
    ('/', LandingPage),
    ('/news', NewsPage),
    ('/roster', RosterPage),
    ('/roster_refresh', CacheCronPage),
], debug=DEBUG)