class Player(object):
    """docstring for Player"""

    name_first_last = ""
    player_id = ""
    position = ""
    status_short = ""
    player_url = ""

    def __init__(self, name_first_last, player_id, position, status_short):
        self.name_first_last = name_first_last
        self.player_id = player_id
        self.position = position
        self.status_short = status_short
        self.player_url = "http://www.mlb.com/team/player.jsp?player_id=%s" % (player_id)