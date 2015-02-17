from feed import Feed

from google.appengine.ext import db
from google.appengine.api import urlfetch

class Player(db.Model):
    """
    docstring for Player
    Responsible for setting up a Model entity
    for the Google Cloud Datastore
    """
    first_last = db.StringProperty()
    player_id = db.StringProperty()
    position = db.StringProperty()
    status_short = db.StringProperty()
    url = db.StringProperty()
    mugshot_url = db.StringProperty()
    thumb = db.BooleanProperty()

class Roster(object):
    """
    docstring for Roster
    Sends HTTP request for JSON at MLB API feed
    Receives and prepares JSON data
    Instantiates Player entities with metadata from JSON
    Puts them into the Google Cloud Datastore, a NoSQL database
    """

    loaded_json = ""
    
    def __init__(self):
        self.load_roster_url()

    def load_roster_url(self):
        """
        Instantiates a Feed object responsible for requesting
        and beginning the parsing of the roster JSON at MLB.com
        """
        ROSTER_URL = "http://www.mlb.com/lookup/json/named.roster_all.bam?team_id=137"
        feed = Feed(ROSTER_URL)
        feed.load_and_prepare()
        succeeded, self.loaded_json = feed.get_representation

    def prepare_players(self):
        """
        Prepares all incoming Player entities from the JSON
        Will attempt to figure out if a thumbnail exists
        Puts resulting object into the database
        """
        self.run = True
        roster_all = self.loaded_json["roster_all"]
        roster_results = roster_all["queryResults"]
        roster_rows = roster_results["row"]

        for plr in roster_rows:
            try:
                name_first_last = plr["name_first_last"]
                player_id = plr["player_id"]
                position = plr["position"]
                status_short = plr["status_short"]
                mugshot_url = ""
                thumb = ""

                result = urlfetch.fetch("http://www.mlb.com/images/players/mugshot/ph_%s.jpg" % (player_id))

                if result.status_code == 404:
                    mugshot_url = "../static/images/mugshot_placeholder.png"
                    thumb = False
                elif result.status_code == 200:
                    mugshot_url = "http://www.mlb.com/images/players/mugshot/ph_%s.jpg" % (player_id)
                    thumb = True
                else:
                    mugshot_url = "None"
                    thumb = False

                p = Player(
                    first_last=name_first_last, 
                    player_id=player_id, 
                    position=position, 
                    status_short=status_short,
                    url=("http://www.mlb.com/team/player.jsp?player_id=%s" % (player_id)),
                    mugshot_url=mugshot_url,
                    thumb=thumb
                )

                p.put()
            except KeyError, e:
                print 'KeyError - reason "%s"' % str(e)