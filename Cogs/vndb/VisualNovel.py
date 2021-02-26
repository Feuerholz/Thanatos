
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
    lengthstrings = {
        1: "<2 hours",
        2: "2-10 hours",
        3: "10-30 hours",
        4: "30-50 hours",
        5: "<50 hours",
        }


    def __init__(self, dict):
        for key in dict:
            if dict [key] is not None:
                setattr(self, key, dict[key])

    def lengthAsString(self):
        return self.lengthstrings.get(self.length, "unknown")

    def formattedLanguages(self):
        if (self.orig_lang[0] is None):
            return "none"
        langstring = "**{0}**".format(self.orig_lang[0])
        for lang in self.languages:
            if(lang==self.orig_lang[0]):
                continue
            langstring += ", {0}".format(lang)
        return langstring

    def formattedPlatforms(self):
        if (self.platforms is None):
            return "none"
        platstring = self.platforms[0]
        for platform in self.platforms[1:]:
            platstring += ", {0}".format(platform)
        return platstring