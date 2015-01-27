class Player(object):
    """docstring for Player"""

    name_first_last = ""
    player_id = ""
    position = ""
    status_short = ""
    player_url = ""
    player_banner = ""

    def __init__(self, name_first_last, player_id, position, status_short):
        self.name_first_last = name_first_last
        self.player_id = player_id
        self.position = position
        self.status_short = status_short
        self.player_url = "http://www.mlb.com/team/player.jsp?player_id=%s" % (player_id)
        self.player_banner = "http://giants.mlb.com/images/players/525x330/%s.jpg" % (player_id)