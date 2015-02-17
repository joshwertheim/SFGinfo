class NewsStory(object):
    """
    docstring for NewsStory
    Currently has minimum setup for metadata for stories
    Class will be expanded later when more news sources
    are added
    """
    
    althead = ""
    blurb = ""
    story_url = ""

    def __init__(self, althead, blurb, story_url):
        self.althead = althead
        self.blurb = blurb
        self.story_url = story_url