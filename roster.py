from feed import Feed

class Roster(object):
    """docstring for Roster"""

    loaded_json = ""
    roster_list = list()
    
    def __init__(self):
        self.load_roster_url()

    def load_roster_url(self):
        ROSTER_URL = "http://www.mlb.com/lookup/json/named.roster_all.bam?team_id=137"
        feed = Feed(ROSTER_URL)
        feed.load_and_prepare()
        succeeded, self.loaded_json = feed.get_representation
        # print feed.formatted_response_data