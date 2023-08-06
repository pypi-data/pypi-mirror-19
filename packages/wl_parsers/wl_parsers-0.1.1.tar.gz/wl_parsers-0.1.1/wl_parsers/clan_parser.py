# Imports

## parser_core - core parser class
from parser_core import *

## requests - to handle HTTP requests
import requests

# Main clan parser class
class ClanParser(WLParser):

    ## constructor
    ### extends WLParser constructor with clan-specific URL
    ###
    ### @PARAMS
    ### 'clanID' (string or integer): ID of targeted clan
    def __init__(self, clanID):
        baseURL = "https://www.warlight.net/Clans/?"
        self.ID = clanID
        self.URL = self.makeURL(baseURL, ID=clanID)

    ## exists
    ### returns True if the clan exists
    @property
    @getPageData
    def exists(self):
        nonexistentMarker = ("-->\n\nOops!  That item could not be found.  "
                             "It may have been deleted.")
        return (nonexistentMarker not in self.pageData)

    ## name
    ### returns the name of a clan
    @property
    @getPageData
    @checkNonexistent
    def name(self):
        page = self.pageData
        return self.getValueFromBetween(page, "<title>", " -")

    ## size
    ### returns a clan's member count
    @property
    @getPageData
    @checkNonexistent
    def size(self):
        page = self.pageData
        marker = "Number of members:</font> "
        return self.getIntegerValue(page, marker)

    ## link
    ### gets URL string for clan's designated link
    @property
    @getPageData
    @checkNonexistent
    def link(self):
        page = self.pageData
        marker = 'Link:</font> <a rel="nofollow" href="'
        end = '">'
        link = self.getValueFromBetween(page, marker, end)
        if link == "http://": return ""
        return link

    ## tagline
    ### returns clan tagline
    @property
    @getPageData
    @checkNonexistent
    def tagline(self):
        page = self.pageData
        marker = 'Tagline:</font> '
        end = '<br />'
        return self.getValueFromBetween(page, marker, end)

    ## createdDate
    ### returns datetime object representing the creation date of a clan
    @property
    @getPageData
    @checkNonexistent
    def createdDate(self):
        page = self.pageData
        marker = "Created:</font> "
        end = "<br"
        dateString = self.getValueFromBetween(page, marker, end)
        return self.getDate(dateString)

    ## bio
    ### returns clan bio from clan page
    @property
    @getPageData
    @checkNonexistent
    def bio(self):
        page = self.pageData
        marker = "Bio:</font>  "
        end = "<br />"
        return self.getValueFromBetween(page, marker, end)

    ## member
    ### returns members of a clan in a list of dictionaries in the format:
    ### {'ID' (int), 'name' (string), 'title' (string),
    ###  'isMember' (bool)}
    @property
    @getPageData
    @checkNonexistent
    def members(self):
        page = self.pageData
        marker = '<table class="dataTable">'
        end = '</table>'
        data = list()
        dataRange = self.getValueFromBetween(page, marker, end)
        dataSet = dataRange.split('<tr>')[2:]
        for dataPoint in dataSet:
            isMember = ('/Images/SmallMemberIcon.png"' in dataPoint)
            playerID = self.getIntegerValue(dataPoint, "/Profile?p=")
            playerName = self.getValueFromBetween(dataPoint,
                         '">', '</a>')
            titleRange = dataPoint.split("<td>")[-1]
            playerTitle = self.getValueFromBetween(titleRange, "",
                          "</td")
            data.append({'ID': playerID, 'name': playerName, 
                         'title': playerTitle, 'isMember': isMember})
        return data

# getClans
## returns a set of all clan IDs on warlight
def getClans():
    URL = "https://www.warlight.net/Clans/List"
    r = requests.get(URL)
    clanSet = set()
    clanData = r.text.split("/Clans/?ID=")[1:]
    for clan in clanData:
        clanID = ""
        while clan[0] in string.digits:
            clanID += clan[0]
            clan = clan[1:]
        clanSet.add(int(clanID))
    return clanSet