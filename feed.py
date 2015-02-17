import urllib2
import json

class Feed(object):
    """
    docstring for Feed
    Takes in a URL as a parameter
    Sends a request for the data at URL
    Begins processing the data
    """
    url = ""
    response_data = ""
    formatted_response_data = ""
    json_representation = ""

    def __init__(self, url):
        """
        Initialize Feed object with a url

        Args:
            url (str): url to process
        """
        self.url = url

    def load_and_prepare(self):
        """
        Tries to request the given url
        Uses a try/except block to catch exceptions,
        such as no data existing.
        """
        try:
            self.response_data = urllib2.urlopen(self.url)
        except:
            self.json_representation = "No data at URL."
            return
        self.formatted_response_data = json.load(self.response_data) 
        self.formatted_response_data = json.dumps(self.formatted_response_data, sort_keys=True, indent=4, separators=(',', ': ')) # pretty printed json file object data
        self.json_representation = json.loads(self.formatted_response_data)

    @property
    def get_representation(self):
        if self.json_representation == "No data at URL.":
            return False, self.json_representation
        else:
            return True, self.json_representation
