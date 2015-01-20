import os
import urllib
import json

import jinja2
import webapp2

from feed import Feed
from newsstory import NewsStory
from roster import Roster
from player import Player

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class RosterPage(webapp2.RequestHandler):
    """docstring for RosterPage"""
    def get(self):
        r = Roster()
        roster_all = r.loaded_json["roster_all"]
        roster_results = roster_all["queryResults"]
        roster_rows = roster_results["row"]

        for plr in roster_rows:
            try:
                name_first_last = plr["name_first_last"]
                player_id = plr["player_id"]
                position = plr["position"]
                status_short = plr["status_short"]
                p = Player(name_first_last, player_id, position, status_short)

                r.roster_list.append(p)
            except KeyError, e:
                print 'KeyError - reason "%s"' % str(e)

        template_values = {
            'players': r.roster_list,
        }

        template = JINJA_ENVIRONMENT.get_template('roster.html')
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

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/news', NewsPage),
    ('/roster', RosterPage),
], debug=True)