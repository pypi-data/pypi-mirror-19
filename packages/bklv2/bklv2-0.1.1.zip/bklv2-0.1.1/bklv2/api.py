# -*- coding: utf-8 -*-

import datetime
import shutil
import requests
import json
import rfc6266


def _gpath( path ):
    """
        "https://test.backlog.jp/" -> "https://test.backlog.jp/"
        "https://test.backlog.jp" -> "https://test.backlog.jp/"
    """
    if path == "":
        return "./"
    elif path.endswith( "/" ):
        return path
    else:
        return path + "/"


def _addkw( dic, k, w ):
    """
        dic[] -> dic[k] = w
    """
    if w != None:
        if isinstance( w, ( tuple, list ) ):
            for i, v in w:
                _addkw( dic, k + "[" + i + "]", v )
        elif isinstance( w, bool ):
            if w == True:
                dic[k] = "true"
            else:
                dic[k] = "false"
        elif isinstance( w, datetime.date ):
                dic[k] = w.strftime( "%Y-%m-%d" )
        else:
            dic[k] = w


def _addkws( dic, k, w ):
    """
        dic[] -> dic[k[]] = w[]
    """
    if w != None:
        if isinstance( w, ( tuple, list ) ):
            i=0
            for v in w:
                _addkw( dic, k + "[" + str(i) + "]", v )
                i+=1
        else:
            _addkw( dic, k + "[0]", w )


def _dicset( dic, k, w, tuples ):
    for t in tuples:
        if k==t:
            _addkws( dic, k[0:-1], w )
            return
    _addkw( dic, k, w )


class api( object ):
    """
    Backlog API version 2 wrapper
    """

    def __init__( self, hostname, apikey ):
        """
            hostname: "https://[spacename].backlog.jp"
            apikey: "nWdhOFxDpAlsFTGSIHisRkUvTq5eTiBDBJ0FFqAdtLTSIvKpfkvb09Kteststring"
        """
        if hostname.endswith( "/" ):
            self.hostname = hostname.rstrip("/")
        else:
            self.hostname = hostname
        self.apikey = apikey


    def _makeurl( self, path ):
        return self.hostname + path


    def _api_return( self, response, **kwargs ):
        self.response = response
        output="json"
        dir_path = "./"
        for k, v in kwargs.items():
            if k == "output":
                output = v
            elif k == "dirpath":
                dirpath = v

        if output == "json":
            try:
                return json.loads( self.response.text )
            except:
                return {}
        elif output == "response":
            return response
        elif output == "path":
            if response.status_code == 200:
                rr = rfc6266.parse_requests_response( response )
                p = _gpath( dirpath ) + rr.filename_unsafe
                with open( p, 'wb' ) as fp:
                    response.raw.decode_content = True
                    shutil.copyfileobj( response.raw, fp )
                return p
        return self.response.text


    def getSpace( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getActivities( self,
                       activityTypeIds = None,
                       minId = None,
                       maxId = None,
                       count = None,
                       order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-activities
        """
        params = { "apiKey": self.apikey }
        _addkws( params, "activityTypeId", activityTypeIds )
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/space/activities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getSpaceImage( self,
                       output = "path",
                       dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space-image
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/image" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getSpaceNotification( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space-notification
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/notification" )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateSpaceNotification( self, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-space-notification
        """
        params = { "apiKey": self.apikey }
        data = { "content": content }
        url = self._makeurl( "/api/v2/space/notification" )

        return self._api_return(
            requests.put( url, params = params, data = data ) )


    def getSpaceDiskUsage( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space-diskusage
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/diskUsage" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addAttachment( self, filepath ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-attachment
        """
        params = { "apiKey": self.apikey }
        fp = open( filepath, "rb" )
        files = { "file": [ requests.utils.guess_filename( fp ),
                          fp.read(),
                          "application/octet-stream" ] }
        fp.close()
        url = self._makeurl( "/api/v2/space/attachment" )

        return self._api_return(
            requests.post( url, params = params, files = files ) )


    def getUsers( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-users
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUser( self, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str( userId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def addUser( self, userId, password, name, mailAddress, roleType ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-user
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId, "password": password, "name": name,
                 "mailAddress": mailAddress, "roleType": roleType }
        url = self._makeurl( "/api/v2/users" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateUser( self, userId,
                    password = None,
                    name = None,
                    mailAddress = None,
                    roleType = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-user
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "password", password )
        _addkw( data, "name", name )
        _addkw( data, "mailAddress", mailAddress )
        _addkw( data, "roleType", roleType )
        url = self._makeurl( "/api/v2/users/" + str( userId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteUser( self, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-user
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str( userId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getMyselfUser( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-myself-user
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/myself" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserIcon( self, userId,
                     output = "path",
                     dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-icon
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/icon" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getUserActivities( self, userId,
                           activityTypeIds = None,
                           minId = None,
                           maxId = None,
                           count = None,
                           order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-activities
        """
        params = { "apiKey": self.apikey }
        _addkws( params, "activityTypeIds", activityTypeIds )
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/activities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserStars( self, userId,
                      minId = None,
                      maxId = None,
                      count = None,
                      order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-stars
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/stars" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserStarsCount( self, userId,
                           since = None,
                           until = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-stars-count
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "since", since )
        _addkw( params, "until", until )
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/stars/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserRecentlyViewedIssues( self,
                                     order = None,
                                     offset = None,
                                     count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-recentlyviewedissues
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/users/myself/recentlyViewedIssues" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserRecentlyViewedProjects( self,
                                       order = None,
                                       offset = None,
                                       count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-recentlyviewedprojects
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/users/myself/recentlyViewedProjects" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserRecentlyViewedWikis( self,
                                    order = None,
                                    offset = None,
                                    count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-recentlyviewedwikis
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/users/myself/recentlyViewedWikis" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getGroups( self,
                   order = None,
                   offset = None,
                   count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-groups
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/groups" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addGroup( self, name,
                  members = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-group
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        _addkws( data, "members", members )
        url = self._makeurl( "/api/v2/groups" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getGroup( self, groupId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-group
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateGroup( self, groupId,
                     name = None,
                     members = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-group
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkws( data, "members", members )
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteGroup( self, groupId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-group
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getStatus( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-status
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/statuses" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getResolutions( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-resolutions
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/resolutions" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getPriorities( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-priorities
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/priorities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getProjects( self,
                     archived = None,
                     all = False ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-projects
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "archived", archived )
        _addkw( params, "all", all )
        url = self._makeurl( "/api/v2/projects" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addProject( self, name, key, chartEnabled, subtaskingEnabled, textFormattingRule,
                    projectLeaderCanEditProjectLeader = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project
        """
        params = { "apiKey": self.apikey }
        data = { "name": name, "key": key }
        _addkw( data, "chartEnabled", chartEnabled )
        _addkw( data, "subtaskingEnabled", subtaskingEnabled )
        _addkw( data, "textFormattingRule", textFormattingRule )
        _addkw( data, "projectLeaderCanEditProjectLeader", projectLeaderCanEditProjectLeader )
        url = self._makeurl( "/api/v2/projects" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getProject( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" ) + str( projectIdOrKey )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateProject( self, projectIdOrKey,
                       name = None,
                       key = None,
                       chartEnabled = None,
                       subtaskingEnabled = None,
                       projectLeaderCanEditProjectLeader = None,
                       textFormattingRule = None,
                       archived = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-project
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "key", key )
        _addkw( data, "chartEnabled", chartEnabled )
        _addkw( data, "subtaskingEnabled", subtaskingEnabled )
        _addkw( data, "textFormattingRule", textFormattingRule )
        _addkw( data, "projectLeaderCanEditProjectLeader", projectLeaderCanEditProjectLeader )
        _addkw( data, "archived", archived )
        url = self._makeurl( "/api/v2/projects/" ) + str( projectIdOrKey )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteProject( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" ) + str( projectIdOrKey )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getProjectIcon( self, projectIdOrKey,
                        output = "path",
                        dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-icon
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + "/image" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath  )


    def getProjectActivities( self, projectIdOrKey,
                              activityTypeIds = None,
                              minId = None,
                              maxId = None,
                              count = None,
                              order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-activities
        """
        params = { "apiKey": self.apikey }
        _addkws( params, "activityTypeIds", activityTypeIds )
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/activities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addProjectUser( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project-user
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/users" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getProjectUsers( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-users
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/users" )

        return self._api_return(
            requests.get( url, params = params ) )


    def deleteProjectUser( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-user
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/users" )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def addProjectAdministrator( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project-administrator
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/administrators" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getProjectAdministrators( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-adminnistrators
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/administrators" )

        return self._api_return(
            requests.get( url, params = params ) )


    def deleteProjectAdministrator( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-administrator
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/administrators" )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getIssueTypes( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issuetypes
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addIssueType( self, projectIdOrKey, name, color ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-issuetype
        """
        params = { "apiKey": self.apikey }
        data = { "name": name, "color": color }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateIssueType( self, projectIdOrKey, id,
                         name = None,
                         color = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-issuetype
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "color", color )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes/" + str( id ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteIssueType( self, projectIdOrKey, id, substituteIssueTypeId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issuetype
        """
        params = { "apiKey": self.apikey }
        data = { "substituteIssueTypeId": str( substituteIssueTypeId ) }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes/" + str( id ) )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getCategories( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-categories
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addCategory( self, projectIdOrKey, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-category
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateCategory( self, projectIdOrKey, id, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-category
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories/" + str( id ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteCategory( self, projectIdOrKey, id ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-category
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories/" + str( id ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getVersions( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-versions
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addVersion( self, projectIdOrKey, name,
                    description = None,
                    startDate = None,
                    releaseDueDate = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-version
            startDate,releaseDueDate : YYYY-MM-DD
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        _addkw( data, "description", description )
        _addkw( data, "startDate", startDate )
        _addkw( data, "releaseDueDate", releaseDueDate )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateVersion( self, projectIdOrKey, id, name,
                       description = None,
                       startDate = None,
                       releaseDueDate = None,
                       archived = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-version
            startDate,releaseDueDate : YYYY-MM-DD
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        _addkw( data, "description", description )
        _addkw( data, "startDate", startDate )
        _addkw( data, "releaseDueDate", releaseDueDate )
        _addkw( data, "archived", archived )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions/" + str( id ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteVersion( self, projectIdOrKey, id ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-version
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions/" + str( id ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getCustomfeilds( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-customfields
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addCustomfeild( self, projectIdOrKey, typeId, name, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-customfield
        """
        tuples = ["items", "applicableIssueTypes"]
        params = { "apiKey": self.apikey }
        data = { "typeId": typeId, "name": name }
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateCustomfeild( self, projectIdOrKey, customFeildId, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-customfield
        """
        tuples = ["items", "applicableIssueTypes"]
        params = { "apiKey": self.apikey }
        data = {}
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFeildId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteCustomfeild( self, projectIdOrKey, customFeildId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-customfield
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFeildId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def addCustomfieldItem( self, projectIdOrKey, customFeildId, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-customfield-item
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFeildId ) + \
                             "/items" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateCustomfieldItem( self, projectIdOrKey, customFeildId, itemId, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-customfield-item
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFeildId ) + \
                             "/items/" + str( itemId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteCustomfieldItem( self, projectIdOrKey, customFeildId, itemId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-customfield-item
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFeildId ) + \
                             "/items/" + str( itemId ) )

        return self._api_return(
            requests.delete( url, params = params ) )

    def getSharedfiles( self, projectIdOrKey,
                        path = "",
                        order = None,
                        offset = None,
                        count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-sharedfiles
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "order", order )
        _addkw( data, "offset", offset )
        _addkw( data, "count", count )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/files/metadata/" + str( path ) )

        return self._api_return(
            requests.get( url, params = params, data = data ) )


    def getSharedfile( self, projectIdOrKey, sharedFileId,
                       output = "path",
                       dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-sharedfile
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/files/" + str( sharedFileId ) )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getProjectDiskUsage( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-diskusage
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/diskUsage" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWebhooks( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-webhooks
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWebhook( self, projectIdOrKey, name, hookUrl,
                    description = None,
                    allEvent = None,
                    activityTypeIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-webhook
        """
        params = { "apiKey": self.apikey }
        data = { "name": name, "hookUrl": hookUrl }
        _addkw( data, "description", description )
        _addkw( data, "allEvent", allEvent )
        _addkws( data, "activityTypeIds", activityTypeIds )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getWebhook( self, projectIdOrKey, webhookId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-webhook
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks/" + str( webhookId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateWebhook( self, projectIdOrKey, webhookId,
                       name = None,
                       hookUrl = None,
                       description = None,
                       allEvent = None,
                       activityTypeIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-webhook
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "description", description )
        _addkw( data, "hookUrl", hookUrl )
        _addkw( data, "allEvent", allEvent )
        _addkws( data, "activityTypeIds", activityTypeIds )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks/" + str( webhookId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteWebhook( self, projectIdOrKey, webhookId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-webhook
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks/" + str( webhookId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getIssues( self, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issues
        """
        tuples = [ "projectIds", "issueTypeIds", "categoryIds", "versionIds", \
                   "milestoneIds", "statusIds", "priorityIds", "assigneeIds", \
                   "createdUserIds", "resolutionIds", "ids", "parentIssueIds" ]
        params = { "apiKey": self.apikey }
        for k, w in kwargs.items():
            _dicset(params,k,w,tuples)
        url = self._makeurl( "/api/v2/issues" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getIssuesCount( self, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issues-count
        """
        tuples = [ "projectIds", "issueTypeIds", "categoryIds", "versionIds", \
                   "milestoneIds", "statusIds", "priorityIds", "assigneeIds", \
                   "createdUserIds", "resolutionIds", "ids", "parentIssueIds" ]
        params = { "apiKey": self.apikey }
        for k, w in kwargs.items():
            _dicset(params,k,w,tuples)
        url = self._makeurl( "/api/v2/issues/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addIssue( self, projectId, summary, issueTypeId, priorityId, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-issue
        """
        tuples = [ "categoryIds", "versionIds", "milestoneIds", "notifiedUserIds", "attachmentIds" ]
        params = { "apiKey": self.apikey }
        data = { "projectId": projectId, "summary": summary, "issueTypeId": issueTypeId, "priorityId": priorityId }
        for k, w in kwargs.items():
            _dicset(data,k,w,tuples)
        url = self._makeurl( "/api/v2/issues" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getIssue( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateIssue( self, issueIdOrKey, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-issue
        """
        tuples = [ "categoryIds", "versionIds", "milestoneIds", "notifiedUserIds", "attachmentIds" ]
        params = { "apiKey": self.apikey }
        data = {}
        for k, w in kwargs.items():
            _dicset(data,k,w,tuples)
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteIssue( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getComments( self, issueIdOrKey,
                     minId = None,
                     maxId = None,
                     count = None,
                     order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-comments
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addComment( self, issueIdOrKey, content,
                    notifiedUserIds = None,
                    attachmentIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-comment
        """
        params = { "apiKey": self.apikey }
        data = {"content": content}
        _addkw( data, "content", content )
        _addkws( data, "notifiedUserId", notifiedUserIds )
        _addkws( data, "attachmentId", attachmentIds )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getCommentsCount( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-comments-count
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getComment( self, issueIdOrKey, commentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-comment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateComment( self, issueIdOrKey, commentId, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-comment
        """
        params = { "apiKey": self.apikey }
        data = { "content": content }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def getCommentNotifications( self, issueIdOrKey, commentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-comment-notifications
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) + \
                             "/notifications" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addCommentNotification( self, issueIdOrKey, commentId, notifiedUserIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-comment-notification
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "notifiedUserId", notifiedUserIds )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) + \
                             "/notifications" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getIssueAttachments( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-attachments
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/attachments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getIssueAttachment( self, issueIdOrKey, attachmentId,
                            output = "path",
                            dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )

    def deleteIssueAttachment( self, issueIdOrKey, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getIssueSharedfiles( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-sharedfiles
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addIssueSharedfile( self, issueIdOrKey, fileIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-comment-notification
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "fileId", fileIds )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def deleteIssueSharedfile( self, issueIdOrKey, fileId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue-sharedfile
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "fileId", fileId )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/sharedFiles/" + str( fileId ) )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getWikis( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wikis
        """
        params = { "apiKey": self.apikey, "projectIdOrKey": projectIdOrKey }
        url = self._makeurl( "/api/v2/wikis" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWikisCount( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wikis-count
        """
        params = { "apiKey": self.apikey, "projectIdOrKey": projectIdOrKey }
        url = self._makeurl( "/api/v2/wikis/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWikiTags( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-tags
        """
        params = { "apiKey": self.apikey, "projectIdOrKey": projectIdOrKey }
        url = self._makeurl( "/api/v2/wikis/tags" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWiki( self, projectId, name, content,
                 mailNotify = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-tags
        """
        params = { "apiKey": self.apikey }
        data = { "projectId": projectId , "name": name, "content": content }
        _addkw( data, "mailNotify", mailNotify )
        url = self._makeurl( "/api/v2/wikis" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getWiki( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateWiki( self, wikiId,
                    name = None,
                    content = None,
                    mailNotify = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-wiki
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "content", content )
        _addkw( data, "mailNotify", mailNotify )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteWiki( self, wikiId,
                    mailNotify = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-wiki
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "mailNotify", mailNotify )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getWikiAttachments( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-attachments
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWikiAttachment( self, wikiId, attachmentIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-wiki-attachment
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "attachmentId", attachmentIds )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getWikiAttachment( self, wikiId, attachmentId,
                           output = "path",
                           dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )

    def deleteWikiAttachment( self, wikiId, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-wiki-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getWikiSharedfiles( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-sharedfiles
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWikiSharedfile( self, wikiId, fileIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-wiki-sharedfile
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "fileId", fileIds )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def deleteWikiSharedfile( self, wikiId, fileId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-wiki-sharedfile
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/sharedFiles/" + str( fileId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getWikiHistory( self, wikiId,
                        minId = None,
                        maxId = None,
                        count = None,
                        order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-history
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + "/history" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWikiStars( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-stars
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + "/stars" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addStar( self,
                 issueId = None,
                 commentId = None,
                 wikiId = None,
                 pullRequestsId = None,
                 pullRequestCommentId = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-star
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "issueId", issueId )
        _addkw( data, "commentId", commentId )
        _addkw( data, "wikiId", wikiId )
        _addkw( data, "pullRequestsId", pullRequestsId )
        _addkw( data, "pullRequestCommentId", pullRequestCommentId )
        url = self._makeurl( "/api/v2/stars" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getNotification( self,
                         minId = None,
                         maxId = None,
                         count = None,
                         order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-notifications
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/notifications" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getNotificationCount( self,
                              alreadyRead = None,
                              resourceAlreadyRead = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-notifications-count
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "alreadyRead", alreadyRead )
        _addkw( params, "resourceAlreadyRead", resourceAlreadyRead )
        url = self._makeurl( "/api/v2/notifications/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def markAsreadNotifications( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-stars
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/notifications/markAsRead" )

        return self._api_return(
            requests.post( url, params = params ) )


    def markAsreadNotification( self, notificationId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/markasread-notification
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/notifications/" + str( notificationId ) + \
                             "/markAsRead" )

        return self._api_return(
            requests.post( url, params = params ) )


    def getGitRepositories( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-git-repositories
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getGitRepository( self, projectIdOrKey, repoIdOrName ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-git-repository
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) )

        return self._api_return(
            requests.get( url, params = params ) )


    def getPullRequests( self, projectIdOrKey, repoIdOrName ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-requests
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getPullRequestsCount( self, projectIdOrKey, repoIdOrName ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-requests-count
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addPullRequest( self, projectIdOrKey, repoIdOrName, summary, description, base, branch, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-pull-request
        """
        tuples = ["notifiedUserIds","attachmentIds"]
        params = { "apiKey": self.apikey }
        data = { "summary": summary, "description": description , "base": base, "branch ": branch }
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getPullRequest( self, projectIdOrKey, repoIdOrName, number ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updatePullRequest( self, projectIdOrKey, repoIdOrName, number, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-pull-request
        """
        tuples = ["notifiedUserIds"]
        params = { "apiKey": self.apikey }
        data = {}
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def getPullRequestComment( self, projectIdOrKey, repoIdOrName, number,
                               minId = None,
                               maxId = None,
                               count = None,
                               order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-comment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/comments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addPullRequestComment( self, projectIdOrKey, repoIdOrName, number, content, notifiedUserIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-pull-request-comment
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( params, "content", content )
        _addkws( params, "notifiedUserId", notifiedUserIds )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/comments" )

        return self._api_return(
            requests.post( url, params = params ) )


    def getPullRequestCommentsCount( self, projectIdOrKey, repoIdOrName, number ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-comments-count
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/comments/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def updatePullRequestComment( self, projectIdOrKey, repoIdOrName, number, commentId, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-comment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + \
                             "/comments/" + str(commentId) )

        return self._api_return(
            requests.patch( url, params = params ) )


    def getPullRequestAttachments( self, projectIdOrKey, repoIdOrName, number ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-attachments
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/attachments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getPullRequestAttachment( self, projectIdOrKey, repoIdOrName, number, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-attachment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + \
                             "/attachments/" + str(attachmentId) )

        return self._api_return(
            requests.get( url, params = params ) )


    def deletePullRequestAttachment( self, projectIdOrKey, repoIdOrName, number, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-pull-request-attachment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + \
                             "/attachments/" + str(attachmentId) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getWatchingList( self, userId,
                         order = "desc",
                         sort = "issuerUpdated",
                         count = 20,
                         offset = None,
                         resourceAlreadyRead = None,
                         issueIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-watching-list
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "sort", sort )
        _addkw( params, "count", count )
        _addkw( params, "offset", offset )
        _addkw( params, "resourceAlreadyRead", resourceAlreadyRead )
        _addkws( params, "issueIds", issueIds )
        url = self._makeurl( "/api/v2/users/" + str(userId) + "/watchings" )

        return self._api_return(
            requests.get( url, params = params ) )


    def countWatching( self, userId,
                       resourceAlreadyRead = None,
                       alreadyRead = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-watching
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "resourceAlreadyRead", resourceAlreadyRead )
        _addkw( params, "alreadyRead", alreadyRead )
        url = self._makeurl( "/api/v2/users/" + str(userId) + "/watchings/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWatching( self, watchingId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-watching
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/watchings/" + str(watchingId) )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWatching( self, issueIdOrKey, note = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-watching
        """
        params = { "apiKey": self.apikey, "issueIdOrKey" : issueIdOrKey }
        _addkw( params, "note", note )
        url = self._makeurl( "/api/v2/watchings" )

        return self._api_return(
            requests.post( url, params = params ) )


    def updateWatching( self, watchingId, note ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-watching
        """
        params = { "apiKey": self.apikey }
        data = { "note" : note }
        url = self._makeurl( "/api/v2/watchings/" + str(watchingId) )

        return self._api_return(
            requests.patch( url, params = params ) )


    def deleteWatching( self, watchingId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-watching
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/watchings/" + str(watchingId) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def readWatching( self, watchId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/read-watching
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/watchings/" + str(watchId) + "/markAsRead" )

        return self._api_return(
            requests.post( url, params = params ) )


    def checkedWatchings( self, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/checked-watchings
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str(userId) + "/watchings/markAsChecked" )

        return self._api_return(
            requests.post( url, params = params ) )
