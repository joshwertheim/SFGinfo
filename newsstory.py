class NewsStory(object):
    """docstring for NewsStory"""
    
    althead = ""
    blurb = ""
    story_url = ""

    def __init__(self, althead, blurb, story_url):
        self.althead = althead
        self.blurb = blurb
        self.story_url = story_url