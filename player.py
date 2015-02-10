from feed import Feed

from google.appengine.ext import db
from google.appengine.api import urlfetch

class Player(db.Model):
    first_last = db.StringProperty()
    player_id = db.StringProperty()
    position = db.StringProperty()
    status_short = db.StringProperty()
    url = db.StringProperty()
    mugshot_url = db.StringProperty()
    thumb = db.BooleanProperty()

class Roster(object):
    """docstring for Roster"""

    loaded_json = ""
    
    def __init__(self):
        self.load_roster_url()
        # self.prepare_players()


    def load_roster_url(self):
        ROSTER_URL = "http://www.mlb.com/lookup/json/named.roster_all.bam?team_id=137"
        feed = Feed(ROSTER_URL)
        feed.load_and_prepare()
        succeeded, self.loaded_json = feed.get_representation
        # print feed.formatted_response_data

    def prepare_players(self):
        print 'testing'

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


# from google.appengine.api import urlfetch

# class Player(object):
#     """docstring for Player"""

#     name_first_last = ""
#     player_id = ""
#     position = ""
#     status_short = ""
#     player_url = ""
#     player_banner = ""
#     player_mugshot_url = ""

#     def __init__(self, name_first_last, player_id, position, status_short):
#         self.name_first_last = name_first_last
#         self.player_id = player_id
#         self.position = position
#         self.status_short = status_short
#         self.player_url = "http://www.mlb.com/team/player.jsp?player_id=%s" % (player_id)
#         self.player_banner = "http://giants.mlb.com/images/players/525x330/%s.jpg" % (player_id)

        # result = urlfetch.fetch("http://www.mlb.com/images/players/mugshot/ph_%s.jpg" % (player_id))

        # if result.status_code == 404:
        #     self.player_mugshot_url = "../static/images/mugshot_placeholder.png"
        # else:
        #     self.player_mugshot_url = "http://www.mlb.com/images/players/mugshot/ph_%s.jpg" % (player_id)