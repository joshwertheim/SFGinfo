import os
import urllib
import json

import jinja2
import webapp2

from feed import Feed
from newsstory import NewsStory

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
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
    ('/', MainPage),
], debug=True)