# Imports
# core parser class and functions
from parser_core import *

# main player parser class
class PlayerParser(WLParser):

    ## constructor
    ### takes a player ID
    def __init__(self, playerID):
        baseURL = "https://www.warlight.net/Profile?"
        self.ID = playerID
        self.URL = self.makeURL(baseURL, p=playerID)

    ## exists
    ### returns a boolean determining whether a player exists
    @property
    @getPageData
    def exists(self):
        page = self.pageData
        marker = "Sorry, the requested player was not found."
        return (marker not in page)

    ## inClan
    ### returns True if the player is in a clan,
    ### False otherwise
    ### remember that nonexistent players will return None
    @property
    @getPageData
    @checkNonexistent
    def inClan(self):
        return self.clanID is not None

    ## clanID
    ### returns ID number for player's clan
    @property
    @getPageData
    @checkNonexistent
    def clanID(self):
        page = self.pageData
        marker = '<a href="/Clans/?ID='
        if marker not in page: return None
        return self.getIntegerValue(page, marker)

    ## clanIcon
    ### returns URL string for clan icon
    @property
    @getPageData
    @checkNonexistent
    def clanIcon(self):
        page = self.pageData
        marker = '"vertical-align: middle" src="'
        end = '" border="'
        if marker not in page: return None
        return self.getValueFromBetween(page, marker, end)

    ## location
    ### returns location string for a player
    ### either a country name or "United States: [state name]"
    @property
    @getPageData
    @checkNonexistent
    def location(self):
        page = self.pageData
        marker = 'title="Plays from '
        end = '"'
        if marker not in page: return ""
        return self.getValueFromBetween(page, marker, end)

    ## clanName
    ### returns name (string) of player's clan
    @property
    @getPageData
    @checkNonexistent
    def clanName(self):
        page = self.pageData
        outerMarker = '<a href="/Clans/?ID='
        if outerMarker not in page: return ""
        outerEnd = '/a>'
        clanNameArea = self.getValueFromBetween(page, outerMarker, outerEnd)
        innerMarker = 'border="0" />'
        innerEnd = '<'
        if innerMarker in clanNameArea:
            return self.trimString(self.getValueFromBetween(clanNameArea,
                                                            innerMarker,
                                                            innerEnd))
        else:
            otherMarker = '">'
            otherEnd = '<'
            return self.trimString(self.getValueFromBetween(clanNameArea,
                                                            otherMarker,
                                                            otherEnd))

    ## name
    ### gets player's name
    ### raises ContentError if player does not exist
    @property
    @getPageData
    @checkNonexistent
    def name(self):
        page = self.pageData
        return self.getValueFromBetween(page, '<title>', ' -')

    ## isMember
    ### returns boolean (True if user is a Member)
    @property
    @getPageData
    @checkNonexistent
    def isMember(self):
        page = self.pageData
        memberString = 'id="MemberIcon" title="WarLight Member"'
        return (memberString in page)

    ## level
    ### returns player's level
    @property
    @getPageData
    @checkNonexistent
    def level(self):
        page = self.pageData
        return self.getIntegerValue(page, '<big><b>Level ')

    ## points
    ### returns points earned in last 30 days (int)
    @property
    @getPageData
    @checkNonexistent
    def points(self):
        page = self.pageData
        points = self.getTypedValue(page, 'days:</font> ',
                                    (string.digits + ","))
        return int(points.replace(",",""))

    ## email
    ### returns player (partial) e-mail as a string
    @property
    @getPageData
    @checkNonexistent
    def email(self):
        page = self.pageData
        marker = "E-mail:</font> "
        end = "<br />"
        return self.getValueFromBetween(page, marker, end)

    ## link
    ### returns player-supplied link as a string
    @property
    @getPageData
    @checkNonexistent
    def link(self):
        page = self.pageData
        marker = "Player-supplied link:"
        end = "</a>"
        dataRange = self.getValueFromBetween(page, marker, end)
        return self.getValueFromBetween(dataRange, '">', None)

    ## tagline
    ### returns player tagline as a string
    @property
    @getPageData
    @checkNonexistent
    def tagline(self):
        page = self.pageData
        marker = "Tagline:</font> "
        end = "<br />"
        return self.getValueFromBetween(page, marker, end)

    ## bio
    ### returns player bio as a string
    @property
    @getPageData
    @checkNonexistent
    def bio(self):
        page = self.pageData
        marker = "Bio:</font>  "
        end = "<br />"
        return self.trimString(self.getValueFromBetween(page, marker, end))

    ## getJoinString
    ### returns player join date as a string
    ### formatted mm/dd/yyyy
    @getPageData
    @checkNonexistent
    def getJoinString(self):
        page = self.pageData
        marker = "Joined WarLight:</font> "
        end = "<br />"
        return self.getValueFromBetween(page, marker, end)
        
    ## joinDate
    ### returns player join date as a datetime object
    @property
    @getPageData
    @checkNonexistent
    def joinDate(self):
        return self.getDate(self.getJoinString())

    ## getMemberString
    ### returns player membership date as a string
    ### formatted mm/dd/yyyy
    @getPageData
    @checkNonexistent
    def getMemberString(self):
        page = self.pageData
        marker = "Member since</font> "
        end = "</font>"
        if marker not in page: return ""
        return self.getValueFromBetween(page, marker, end)

    ## memberSince
    ### returns player membership date as a datetime object
    ### if player is not a member, returns None
    @property
    @getPageData
    @checkNonexistent
    def memberSince(self):
        memberString = self.getMemberString()
        if memberString == "": return None
        return self.getDate(memberString)

    ## currentGames
    ### returns integer amount of ongoing multi-day 
    @property
    @getPageData
    @checkNonexistent
    def currentGames(self):
        page = self.pageData
        dataRange = self.getValueFromBetween(page, 
                    "Currently in</font> ", "games")
        if "multi-day" not in dataRange: return 0
        return self.getIntegerValue(dataRange, "")

    ## playedGames
    ### returns integer amount of played games
    @property
    @getPageData
    @checkNonexistent
    def playedGames(self):
        page = self.pageData
        return self.getIntegerValue(page, "Played in</font> ")

    ## percentRT
    ### returns float percentage of real-time games (relative to played)
    @property
    @getPageData
    @checkNonexistent
    def percentRT(self):
        page = self.pageData
        dataRange = self.getValueFromBetween(page, "Played in",
                                             "<br />")
        return self.getNumericValue(dataRange, " (")

    ## getLastSeenString
    ### returns string indicating time since user last performed
    ### an action; minimum value is "less than 15 minutes ago"
    @getPageData
    @checkNonexistent
    def getLastSeenString(self):
        page = self.pageData
        marker = "Last seen </font>"
        end = "<font"
        return self.trimString(self.getValueFromBetween(page,
                                                 marker, end))

    ## lastSeen
    ### returns floating-point value representing
    ### time since user was last online, in hours
    @property
    @getPageData
    @checkNonexistent
    def lastSeen(self):
        lastSeenString = self.getLastSeenString()
        if "less than" in lastSeenString:
            return 0
        return self.timeConvert(lastSeenString)

    ## bootCount
    ### returns number of times a player has been booted
    @property
    @getPageData
    @checkNonexistent
    def bootCount(self):
        page = self.pageData
        if "never been booted" in page: return 0
        marker = "This player has been booted "
        return self.getIntegerValue(page, marker)

    ## bootRate
    ### returns percentage of time that a player has been booted
    ### as a floating-point value
    @property
    @getPageData
    @checkNonexistent
    def bootRate(self):
        page = self.pageData
        if "never been booted" in page: return 0.0
        marker = "This player has been booted "
        end = "</font>"
        dataRange = self.getValueFromBetween(page, marker, end)
        return self.getNumericValue(dataRange, " (")

    ## singlePlayerStats
    ### returns a player's single-player stats as a dictionary
    ### formatted {'level name': {'turns': # of turns, 'gold star': (bool)}}
    @property
    @getPageData
    @checkNonexistent
    def singlePlayerStats(self):
        page = self.pageData
        marker = "<h3>Single-player stats</h3>"
        gsMarker = 'img src="/Images/GoldStar.png"'
        data = dict()
        if marker not in page: return data
        dataRange = self.getValueFromBetween(page, marker, "<h3")
        dataSet = dataRange.split('color="#858585')[1:]
        for dataPoint in dataSet:
            levelName = self.getValueFromBetween(dataPoint, '">',
                        ':</font>')
            levelTurns = self.getIntegerValue(dataPoint, "Won in ")
            data[levelName] = {'turns': levelTurns,
                               'gold star': (gsMarker in dataPoint)}
        return data

    ## favoriteGames
    ### returns a player's favorite games in a list of dictionaries:
    ### {'ID': ID (integer), 'name': name (string)}
    @property
    @getPageData
    @checkNonexistent
    def favoriteGames(self):
        page = self.pageData
        data = list()
        marker = "<h3>Favorite Games</h3>"
        if marker not in page: return data
        end = "<h3>"
        dataRange = self.getValueFromBetween(page, marker, end)
        dataSet = dataRange.split("GameID=")[1:]
        for dataPoint in dataSet:
            gameID = self.getIntegerValue(dataPoint, "")
            gameName = self.getValueFromBetween(dataPoint,
                       '">', "</a>")
            gameData = {'ID': gameID, 'name': gameName}
            data.append(gameData)
        return data

    ## favoriteTournaments
    ### returns a player's favorite tournaments in a list of dictionaries
    ### {'ID': ID (integer), 'name': name (string), 'rank': rank of player (int)}
    ### if a player isn't ranked, rank is set to None
    @property
    @getPageData
    @checkNonexistent
    def favoriteTournaments(self):
        page = self.pageData
        marker = "<h3>Tournaments</h3>"
        data = list()
        if marker not in page: return data
        dataRange = self.getValueFromBetween(page, marker, "<h3")
        dataSet = dataRange.split("- ")[1:]
        for dataPoint in dataSet:
            if dataPoint[0] in string.digits:
                rank = self.getIntegerValue(dataPoint, "")
            else: rank = None
            tourneyID = self.getIntegerValue(dataPoint,
                        "TournamentID=")
            tourneyName = self.getValueFromBetween(dataPoint, '">',
                          "</a>")
            data.append({'ID': tourneyID, 'name': tourneyName, 'rank': rank})
        return data

    ## ladderData
    ### fetches a player's ladder data in a dictionary
    ### output[ladder name] is a dictionary
    ### {'team': teamID (integer), 'rank': rank (integer),
    ###  'rating': rating (integer), 'peak rank': (integer),
    ###  'peak rating': (integer)}
    ### rank, rating, peakRank, peakRating are None if inapplicable
    @property
    @getPageData
    @checkNonexistent
    def ladderData(self):
        page = self.pageData
        marker = "<h3>Ladder Statistics</h3>"
        data = dict()
        if marker not in page: return data
        dataRange = self.getValueFromBetween(page, marker, "<h3")
        dataSet = dataRange.split("a href=")[1:]
        for dataPoint in dataSet:
            teamID = self.getIntegerValue(dataPoint, "TeamID=")
            ladderName = self.getValueFromBetween(dataPoint, '">',
                         "</a>")
            if ("Not Ranked" in dataPoint):
                rank = None
            else: rank = self.getIntegerValue(dataPoint, "Ranked ")
            rating = self.getIntegerValue(dataPoint, "rating of ")
            if ("Best rating ever:" not in dataPoint):
                peakRating = None
            else: peakRating = self.getIntegerValue(dataPoint,
                               "Best rating ever: ")
            if ("best rank ever: " not in dataPoint):
                peakRank = None
            else: peakRank = self.getIntegerValue(dataPoint,
                             "best rank ever: ")
            data[ladderName] = {'team': teamID, 'rank': rank, 'rating': rating, 
                                'peak rank': peakRank, 'peak rating': peakRating}
        return data

    ## rankedGames
    ### returns a player's ranked data as a dictionary
    ### output['data'][gameType] is a dictionary
    ### {'wins' (int), 'games' (int), 'win percent' (float)}
    ### output['wins'] (integer): total ranked wins
    ### output['games'] (integer): total ranked games
    ### output['win percent'] (float): win percent for all ranked games
    @property
    @getPageData
    @checkNonexistent
    def rankedGames(self):
        page = self.pageData
        marker = "<h3>Ranked Games</h3>"
        data = dict()
        if marker not in page: 
            return {'data': data, 'wins': None, 'games': None, 'win percent': None}
        dataRange = self.getValueFromBetween(page, marker, "<h3")
        if "No completed ranked games" in dataRange:
            return {'data': data, 'wins': 0, 'games': 0, 'win percent': 0.0}
        rankedCount = self.getIntegerValue(dataRange,
                      "Completed</font> ")
        if "ranked games (" in dataRange:
            rankedWins = self.getIntegerValue(dataRange,
                         "ranked games (")
        else:
            rankedWins = self.getIntegerValue(dataRange,
                         "ranked game (")
        rankedPercent = Decimal(rankedWins) / Decimal(rankedCount)
        rankedPercent = float(rankedPercent * Decimal(100))
        dataSet = dataRange.split('color="#858585"')[2:]
        for dataPoint in dataSet:
            gameType = self.getValueFromBetween(dataPoint,
                       '>', ':</font')
            gamesWon = self.getIntegerValue(dataPoint,
                       "</font> ")
            gamesPlayed = self.getIntegerValue(dataPoint,
                          " / ")
            winPercent = Decimal(gamesWon) / Decimal(gamesPlayed)
            winPercent = float(winPercent * Decimal(100))
            data[gameType] = {'wins': gamesWon,
                              'games': gamesPlayed,
                              'win percent': winPercent}
        return {'data': data, 'wins': rankedWins,
                'games': rankedCount, 'win percent': rankedPercent}

    ## previousNames
    ### returns a list of previous names as dictionaries
    ### {'name': previous name (string), 'date': date of change (date object)}
    @property
    @getPageData
    @checkNonexistent
    def previousNames(self):
        page = self.pageData
        marker = "<h3>Previously known as..."
        data = list()
        if marker not in page: return data
        dataRange = self.getValueFromBetween(page, marker, "<h3")
        dataSet = dataRange.split('&nbsp;&nbsp;&nbsp;')[1:]
        for dataPoint in dataSet:
            name = self.getValueFromBetween(dataPoint, None, " <font")
            untilString = self.getValueFromBetween(dataPoint,
                          '"gray">(', ")")
            until = self.getDate(untilString)
            data.append({'name': name, 'date': until})
        return data

    ## playSpeed
    ### returns play speed as a dictionary
    ### output[type]: average time (in hours)
    ### type is either "Multi-Day Games" or "Real-Time Games"
    @property
    @getPageData
    @checkNonexistent
    def playSpeed(self):
        page = self.pageData
        marker = "<h3>Play Speed</h3>"
        data = dict()
        if marker not in page: return data
        dataRange = self.getValueFromBetween(page, marker, "<h3")
        typeMarkers = ["Multi-Day Games:", "Real-Time Games:"]
        for typeMarker in typeMarkers:
            markedRange = self.getValueFromBetween(dataRange,
                          typeMarker, "<h5")
            avgString = self.getValueFromBetween(markedRange,
                        "Average:</font> ", "<br />")
            avgTime = self.timeConvert(avgString)
            data[typeMarker[:-1]] = avgTime
        return data
 
    ## favoriteMaps
    ### returns a player's favorite maps as a list of dictionaries
    ### {'name': (string), 'author': name (string), 'link': URL to map (str)}
    @property
    @getPageData
    @checkNonexistent
    def favoriteMaps(self):
        page = self.pageData
        baseURL = "https://warlight.net"
        marker = "Favorite Maps</h3>"
        data = list()
        if marker not in page: return data
        dataRange = self.getValueFromBetween(page, marker, "</td")
        dataSet = dataRange.split('a href="')[1:]
        for dataPoint in dataSet:
            link = self.getValueFromBetween(dataPoint, '', '">')
            name = self.getValueFromBetween(dataPoint, 
                   "</a> <br>", "<br>")
            author = self.getValueFromBetween(dataPoint, "by ",
                     "</font>")
            data.append({'name': name, 'author': author, 'link': baseURL+link})
        return data

    ## achievementRate
    ### returns integer % value representing achievements completed
    @property
    @getPageData
    @checkNonexistent
    def achievementRate(self):
        page = self.pageData
        marker = "<h3>Achievements"
        if marker not in page: return 0
        dataRange = self.getValueFromBetween(page, marker, 
                    "</font>")
        return self.getIntegerValue(dataRange, "(")