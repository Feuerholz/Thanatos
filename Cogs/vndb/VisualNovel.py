
#For reference about the meaning and data format of each class member, visit https://vndb.org/d11, 5.1
class VisualNovel():
    id = None              
    title = None
    original = ""
    released = "No data"
    languages = None
    orig_lang = None
    platforms = None
    aliaes = ""
    length = 0
    description = "No description available"
    links = {"wikipedia" : None, "encubed" : None, "renai" : None, "wikidata" : None}
    image = None #TODO: Should replace this with some default image later
    image_nsfw = None   #It says this is deprecated but lets include it just in case
    image_flagging = {"votecount" : 0, "sexual_avg": 2.0, "violence_avg": 2.0} #default the average ratings to maximum to be safe
    anime = None
    relations = None
    tags = None
    popularity = None
    rating = None
    votecount = None
    screens = None
    staff = None



    def __init__(self, dict):
        for key in dict:
            if dict [key] is not None:
                setattr(self, key, dict[key])

