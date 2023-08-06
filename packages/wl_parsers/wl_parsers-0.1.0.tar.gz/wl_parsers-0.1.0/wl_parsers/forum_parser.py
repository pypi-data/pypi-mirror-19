# Imports

## parser core - mainly the core parser class
from parser_core import *

## getErrorFree
### function decorator to retrieve
### an error free page
def getErrorFree(func):
    def func_wrapper(self, *args):
        if (not(hasattr(self, 'isErrorPage'))):
            return func(self, *args)
        else:
            while (self.isErrorPage):
                self.getData()
            return func(self, *args)
    return func_wrapper

# main forum parser class
class ForumPageParser(WLParser):

    ## constructor
    ### takes a forum thread ID and offset
    def __init__(self, threadID, offset):
        baseURL = ("https://www.warlight.net/Forum/" + 
                        str(threadID) + "?")
        self.ID = threadID
        self.offset = offset
        self.URL = self.makeURL(baseURL, Offset=offset)

    ## length
    ### returns integer amount of total comments in thread
    @property
    @getPageData
    @checkNonexistent
    def length(self):
        page = self.pageData
        marker = "Posts "
        end = "&nbsp;"
        contentArea = self.getValueFromBetween(page, marker, end)
        return self.getIntegerValue(contentArea, "of ")

    ## exists
    ### returns a boolean determining whether a thread exists
    @property
    @getPageData
    def exists(self):
        page = self.pageData
        marker = "Oops!  That thread doesn't exist. It may have been deleted."
        altMarker = "Not Found</pre></p><hr><i><small>Powered"
        return (marker not in page and altMarker not in page)

    ## isErrorPage
    ### returns True if a page is the Warlight error page
    @property
    @getPageData
    @checkNonexistent
    def isErrorPage(self):
        page = self.pageData
        errorMarker = '<h1>Whoops, an error has occurred</h1>'
        return (errorMarker in page)

    ## pageExists
    ### returns a boolean determining whether a page is empty
    @property
    @getPageData
    @getErrorFree
    @checkNonexistent
    def pageExists(self):
        page = self.pageData
        return (self.postCount > 0)

    ## postCount
    ### returns the number of posts on page (integer)
    @property
    @getPageData
    @getErrorFree
    @checkNonexistent
    def postCount(self):
        pageLength = max(self.offset, self.length)
        return min(20, pageLength-self.offset)

    ## title
    ### returns thread title as a string
    @property
    @getPageData
    @getErrorFree
    @checkNonexistent
    def title(self):
        before = "<title>"
        after = " - Play Risk"
        return self.getValueFromBetween(self.pageData,
                                        before, after)

    ## parsePost
    ### parses a single post
    ### returns a dictionary:
    ### {'ID' (int), 'author' (dictionary), 'title' (string),
    ###  'message' (string), 'time' (datetime object)}
    ### author: {'ID' (int), 'name' (str),
    ###          'isMember' (bool), 'clan' (dict or None)}
    ### clan: {'ID' (int), 'name'}
    @getPageData
    @getErrorFree
    @checkNonexistent
    def parsePost(self, post):
        idMarker = "PostForDisplay_"
        ID = self.getIntegerValue(post, idMarker)
        titleMarker, titleEnd = '<font color="#CCCCCC">', '</font>'
        title = self.getValueFromBetween(post, titleMarker, titleEnd)
        msgStart, msgEnd = '"PostForDisplay_' + str(ID) + '">', '</div>'
        message = self.trimString(self.getValueFromBetween(post, 
                                  msgStart, msgEnd))
        timeStringStart, timeStringEnd = '</font>:', '</th>'
        timeString = self.trimString(self.getValueFromBetween(
                                     post, timeStringStart, timeStringEnd))
        time = self.getDateTime(timeString)
        authorID = self.getIntegerValue(post, 'Profile?p=')
        authorStart, authorEnd = str(authorID) + '">', '</a>'
        authorName = self.getValueFromBetween(post, authorStart,
                                              authorEnd)
        memberMarker = 'Images/SmallMemberIcon.png'
        memberStatus = (memberMarker in post)
        clanMarker = '/Clans/?ID='
        if clanMarker in post:
            clanID = self.getIntegerValue(post, clanMarker)
            clanNameMarker = clanMarker + str(clanID) + '" title="'
            clanNameEnd = '"><img'
            if(clanNameMarker in post and clanNameEnd in post):
                clanName = self.getValueFromBetween(post, clanNameMarker,
                                                    clanNameEnd)
                clan = {'ID': clanID, 'name': clanName}
            else: clan = None
        else: clan = None
        author = {'ID': authorID, 'name': authorName, 
                  'isMember': memberStatus, 'clan': clan}
        dataPoint = {'ID': ID, 'author': author, 'title': title,
                     'message': message, 'time': time}
        return dataPoint

    ## posts
    ### returns posts on page as a list of dictionaries
    ### {'ID' (int), 'author' (dictionary), 'title' (string),
    ###  'message' (string), 'time' (datetime object),
    ###  'hidden' (bool)}
    ### author: {'ID' (int), 'name' (str),
    ###          'isMember' (bool), 'clan' (dict or None)}
    ### clan: {'ID' (int), 'name'}
    @property
    @getPageData
    @getErrorFree
    @checkNonexistent
    def posts(self):
        if not self.pageExists: return list()
        pageData = self.pageData
        splitter = ('" cellspacing="0" class="region" '
                    'style="padding-bottom:15px; width: 100%;'
                    ' max-width: 900px;')
        postData = pageData.split(splitter)[1:]
        posts = list()
        for post in postData:
            parsed = self.parsePost(post)
            if (("$('#PostTbl_" + str(parsed['ID']) + "').show()'")
                in pageData): 
                parsed['hidden'] = True
            else:
                parsed['hidden'] = False
            posts.append(parsed)
        return posts

# forum thread parser
class ForumThreadParser(object):
    
    ## constructor
    ### takes a thread ID
    def __init__(self, threadID):
        self.ID = threadID

    ## existence check
    @property
    def exists(self):
        return ForumPageParser(self.ID, offset=0).exists

    ## getPages
    ### retrieves page parsers
    @checkNonexistent
    def getPages(self, minOffset=0):
        pages = list()
        threadEnded, offset = False, minOffset
        while (threadEnded is False):
            page = ForumPageParser(self.ID, offset)
            if page.pageExists:
                pages.append(page)
                offset += 20
            else:
                threadEnded = True
        return pages

    ## title
    @property
    @checkNonexistent
    def title(self):
        return ForumPageParser(self.ID, offset=0).title

    ## length
    @property
    @checkNonexistent
    def length(self):
        return ForumPageParser(self.ID, offset=0).length

    ## getPosts
    ### returns a list of dictionaries of posts:
    ### {'ID' (int), 'author' (dictionary), 'title' (string),
    ###  'message' (string), 'time' (datetime object),
    ###  'hidden' (bool)}
    ### author: {'ID' (int), 'name' (str),
    ###          'isMember' (bool), 'clan' (dict or None)}
    ### clan: {'ID' (int), 'name'}
    ###
    ### PARAMS: minOffset (int, optional, default 0)
    @checkNonexistent
    def getPosts(self, minOffset=0):
        pages = self.getPages(minOffset)
        posts = list()
        for page in pages:
            postsInPage = page.posts
            posts += postsInPage
        return posts

# subforum page parser
class SubforumPageParser(WLParser):
    
    ## constructor
    ### needs a forum name
    def __init__(self, forumName, offset):
        if type(forumName) == int:
            forumName = 'f' + str(forumName)
        baseURL = ("https://www.warlight.net/Forum/" + str(forumName) + "?")
        self.URL = self.makeURL(baseURL, Offset=offset)

    ## exists
    ### existence check
    @property
    @getPageData
    def exists(self):
        marker = "Not Found</pre></p><hr><i><small>Powered"
        return (marker not in self.pageData)

    ## threadsExist
    ### returns True if threads exist, False otherwise
    @property
    @getPageData
    @checkNonexistent
    def threadsExist(self):
        threadsMarker = "This forum has no posts."
        return (threadsMarker not in self.pageData)

    ## parseThread
    ### parses a single thread
    @getPageData
    @checkNonexistent
    def parseThread(self, dataPoint):
        threadMarker = '<div id="VotingSpinner_'
        if threadMarker not in dataPoint: return None
        hiddenMarker = 'data-hidden="1" style="display:none"'
        hidden = (hiddenMarker in dataPoint)
        titleBreaker = '<a href="'
        titleLoc = dataPoint.find(titleBreaker)
        dataPoint = dataPoint[titleLoc:]
        title = self.getValueFromBetween(dataPoint,
                '">', '</a>')
        author = self.getValueFromBetween(dataPoint,
                 'by ', "</font>")
        postCount = self.getIntegerValue(dataPoint,
                    '<td nowrap="nowrap">')
        dateBreaker = 'padding-right:15px">'
        dateLoc = dataPoint.find(dateBreaker)
        dataPoint = self.trimString(dataPoint[dateLoc:])
        dateArea = self.getValueFromBetween(dataPoint,
                   '15px">', '<br')
        dateArea = self.trimString(dateArea)
        date = self.getDateTime(self.getValueFromBetween(
                                dateArea, "", ""))
        latestAuthor = self.getValueFromBetween(dataPoint,
                       '#C6C6C6">by ', "</")
        latestPost = {'time': date, 'author name': latestAuthor}
        return {'title': title, 'author name': author, 
                'post count': postCount, 'hidden': hidden,
                'latest post': latestPost}


    ## threads
    ### returns threads on page as a list of dictionaries
    ### {'title', 'author name' (str), 'post count', 'latest post'
    ###  'hidden' (bool)}
    ### latest post: {'time', 'author name' (str)}
    @property
    @getPageData
    @checkNonexistent
    def threads(self):
        threads = list()
        if self.threadsExist == False:
            return threads
        contentBreaker = '<th>Last&nbsp;Post</th>'
        pageLoc = self.pageData.find(contentBreaker)
        pageData = self.pageData[pageLoc:]
        threadSplitter = '<tr'
        threadData = pageData.split(threadSplitter)[1:]
        for dataPoint in threadData:
            thread = self.parseThread(dataPoint)
            if thread is not None:
                threads.append(thread)
        threads = sorted(threads, key=lambda x: x['latest post']['time'])
        threads.reverse() # lowest time at end
        return threads

# subforum parser
## scrapes a whole subforum
class SubforumParser(object):

    ## constructor
    ### takes forumName
    ### forumName can be an integer like 4 (forum #),
    ### a short name like 'f4',
    ### or a full name like 'f4-Map-Development'
    def __init__(self, forumName):
        self.forumName = forumName

    ## existence check
    @property
    def exists(self):
        return SubforumPageParser(self.forumName, offset=0).exists

    ## getPages
    ### generates subforum page parsers and returns them
    ### takes minOffset (default 0) and cutoff (default None)
    @checkNonexistent
    def getPages(self, minOffset=0, cutoff=None):
        pages = list()
        emptyPages, offset = False, minOffset
        while (emptyPages == False):
            pageParser = SubforumPageParser(self.forumName,
                                            offset)
            postsOnPage = pageParser.threadsExist
            if postsOnPage:
                threadsOnPage = pageParser.threads
                firstThreadTime = threadsOnPage[-1]['latest post']['time']
                if cutoff is None or firstThreadTime > cutoff:
                    pages.append(pageParser)
                    offset += 50
                else: # cutoff is not None and firstThreadTime is too old
                    emptyPages = True
            else:
                emptyPages = True
        return pages

    ## getThreads
    ### returns threads as list of dictionaries
    ### in format returned by SubforumPageParser
    ### takes minOffset (default 0)
    ### and cutoff (datetime object, default None)
    @checkNonexistent
    def getThreads(self, minOffset=0, cutoff=None):
        threads = list()
        pages = self.getPages(minOffset, cutoff)
        for page in pages:
            pageThreads = page.threads
            for pageThread in pageThreads:
                if (cutoff is None):
                    threads.append(pageThread)
                elif (cutoff is not None and
                      pageThread['latest post']['time'] > cutoff):
                      threads.append(pageThread)
                else:
                    break # exit loop, no more threads to add
        return threads