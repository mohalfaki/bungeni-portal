#!/usr/bin/env python
# encoding: utf-8
"""
domain.py

Created by Kapil Thangavelu on 2007-11-22.

"""

import md5, random, string

from zope import interface
from ore.alchemist import Session
from alchemist.traversal.managed import ManagedContainer

import interfaces

#####

class Entity( object ):

    @property
    def query( self ):
        return Session().query( self.__class__)
    
class User( object ):
    """
    Domain Object For A User
    """
    
    interface.implements( interfaces.IBungeniUser  )
    
    def __init__( self, login=None, **kw ):
        self.login = login
        self.salt = self._makeSalt()
    
    def _makeSalt( self ):
        return ''.join( random.sample( string.letters, 12) )
        
    def setPassword( self, password ):
        self.password = self.encode( password )
        
    def encode( self, password ):
        return md5.md5( password + self.salt ).hexdigest()
        
    def checkPassword( self, password_attempt ):
        attempt = self.encode( password_attempt )
        return attempt == self.password

    @property
    def name( self ):
        return u"%s %s"%( self.first_name, self.last_name )

class ParliamentMember( User ):
    """ an MP
    """

    # groups

    # committees

    # ministries


    

class HansardReporter( User ):
    """ a reporter who reports on parliamentary procedings
    """

    # rotas

    # takes
    
######    

class Group( object ):
    """ an abstract collection of users
    """
    interface.implements( interfaces.IBungeniGroup )
    
class GroupMembership( object ):
    """ a user's membership in a group
    """
    def __init__( self, user, group ):
        self.user = user
        self.group = group
        
class GroupSitting( object ):
    """ a scheduled meeting for a group (parliament, committee, etc)
    """
    
class GroupSittingAttendance( object ):
    """ a record of attendance at a meeting 
    """
    
class GroupItemAssignment(object):
    """ the assignment of a parliamentary content object to a group
    """

#############

class Government( Group ):
    """ a government
    """

class Parliament( Group ):
    """ a parliament
    """
    mps = ManagedContainer("mps", "bungeni.core.domain.ParliamentMemberContainer", "parliament_id")
    sessions = ManagedContainer("sessions", "bungeni.core.domain.ParliamentSessionContainer", "parliament_id")

class PoliticalParty( Group ):
    """ a political party
    """

class Ministry( Group ):
    """ a government ministry
    """

class Committee( Group ):
    """ a parliamentary committee of MPs
    """
    
#############

class ItemLog( object ):
    """ an audit log of events in the lifecycle of a parliamentary content
    """
    @classmethod
    def makeLogFactory( klass, name ):
        factory = type( name, (klass,), {} )
        return factory

class ItemVersions( object ):
    """a collection of the versions of a parliamentary content object
    """
    @classmethod
    def makeVersionFactory( klass, name ):
        factory = type( name, (klass,), {} )    
        interface.classImplements( factory, interfaces.IVersion )
        return factory
        
class ItemVotes( object ):
    """
    """
    
class ParliamentaryItem( object ):

    interface.implements( interfaces.IBungeniContent )
    # votes

    # schedule

    # object log

    # versions
    pass
    

class Question( ParliamentaryItem ):
    pass


QuestionChange = ItemLog.makeLogFactory( "QuestionChange")
QuestionVersion = ItemVersions.makeVersionFactory("QuestionVersion")


class Motion( ParliamentaryItem ):
    pass

MotionChange = ItemLog.makeLogFactory( "MotionChange")
MotionVersion = ItemVersions.makeVersionFactory("MotionVersion")

class Bill( ParliamentaryItem ):
    pass

BillChange = ItemLog.makeLogFactory( "BillChange")
BillVersion = ItemVersions.makeVersionFactory("BillVersion")


class Constituency( object ):
    """ a locality region, which elects an MP 
    """
    cdetail = ManagedContainer("cdetail", "bungeni.core.domain.ConstituencyDetailContainer", "constituency_id")
    
ConstituencyChange = ItemLog.makeLogFactory( "ConstituencyChange")
ConstituencyVersion = ItemVersions.makeVersionFactory("ConstituencyVersion")

class Region( object ):
    """
    Region of the constituency
    """
    pass
    
class Province( object ):
    """
    Province of the Constituency
    """
    pass
    
class Country( object ):
    """
    Country of Birth
    """ 
    pass   
    
class ConstituencyDetail( object ):
    """
    Details of the Constituency like population and voters at a given time
    """
    pass        

#############

class ParliamentSession( object ):
    """
    """
    sittings = ManagedContainer("sittings", "bungeni.core.domain.GroupSittingContainer", "sessions.session_id")
    
class Rota( object ):
    """
    """

class Take( object ):
    """
    """

class TakeMedia( object ):
    """
    """

class Transcript( object ):
    """
    """    

###############

class ObjectSubscriptions( object ):
    """
    """

