# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Bungeni Alchemist interfaces

$Id$
"""
log = __import__("logging").getLogger("bungeni.alchemist")


# used directly in bungeni
__all__ = [
    "IAlchemistContent",
    "IAlchemistContainer",
    "IDatabaseEngine",
    "IIModelInterface",
    "IModelDescriptor",
    "IModelDescriptorField",
    "IManagedContainer",
    "IContentViewManager",
]


# alchemist.interfaces

from zope.interface import Interface, Attribute
from zope.interface.common.mapping import IEnumerableMapping
from zope import schema

class ITableSchema(Interface):
    """Base interface for autogenerated schemas/interfaces derived from 
    sqlalchemy table definitions.
    """

class IAlchemistContent(ITableSchema):
    """Base interface for autogenerated schemas/interfaces derived from rdb defns.
    
    Provides IIModelInterface, inherits ITableSchema->Interface
    """                 

class IIModelInterface(Interface):
    """Marker interface on generated table schema interfaces, ie. a marker for 
    interfaces. Provided by all "I%TableSchema" interfaces
    """

from zope.app.container.interfaces import IContainer
class IAlchemistContainer(IContainer):
    """A domain record container.
    """
    domain_class = schema.Choice(
        title = u"Domain Class",
        description = u"The Python Path of the Domain Class",
        required = True,
        vocabulary = "Alchemist Domain Classes"
    )
    
    domain_model = Attribute("domain_model", "The domain class")

    def query(**kw):
        """Return the specified children of the container.
        """
        
    def batch(order_by=(), start=0, limit=20):
        """Return a batch of contents with the given offset and size, and 
        ordered by given listing of columns.
        """

class IModelDescriptor(IEnumerableMapping):
    """Captures model behavior encapsulated in a set of fields, which are
    accessible via the enumerable mapping.
    """

class IAlchemistTransmutation(Interface):
    def transmute(schema, **kw):
        """Translates the schema and returns the translation.
        Translations and kw are specific to the translation being performed.
        """

class TransmutationException(Exception):
    """Schema translation exception.
    """

class IDatabaseEngine(Interface):
    """Configuration and access to pooled database connection.
    """


#

from zope.viewlet.interfaces import IViewletManager

# alchemist.security.interfaces
class IAlchemistUser(Interface):
    """The domain class for authentication."""
    def checkPassword(password):
        """Return true if the password matches."""

# alchemist.traversal.interfaces
class IManagedContainer(Interface):
    """ """

# alchemist.ui.interfaces
class IContentViewManager(IViewletManager):
    """Viewlet manager interface."""    


class IModelDescriptorField(Interface):
    # name
    # label
    # description
    modes = schema.ASCIILine(
        title=u"View Usage Modes for Field",
        description=u"Whitespace separated string of different modes."
    )
    # property
    listing_column = schema.Object(Interface,
        title=u"A Custom Column Widget for Listing Views",
        required=False
    )
    listing_column_filter = schema.Object(Interface,
        title=u"A function that filters a listing column on a value",
        required=False
    )
    # !+LISTING_WIDGET(mr, nov-2010) why inconsistently named "listing_column"?
    view_widget = schema.Object(Interface,
        title=u"A Custom Widget Factory for Read Views",
        required=False
    )
    edit_widget = schema.Object(Interface,
        title=u"A Custom Widget Factory for Write Views",
        required=False,
    )
    add_widget = schema.Object(Interface,
        title=u"A Custom Widget Factory for Add Views",
        required=False
    )
    search_widget = schema.Object(Interface,
        title=u"A Custom Search Widget Factory",
        required=False
    )
    ''' !+FIELD_PERMISSIONS(mr, nov-2010) these params are deprecated -- when 
    applied to any field (that corresponds to an attribute of the domain's 
    class), the domain.zcml setting for that same class attribute will anyway 
    take precedence.

    view_permission = schema.ASCIILine(
        title=u"Read Permission",
        description=u"If the user does not have this permission this field "
            "will not appear in read views",
        required=False
    )
    edit_permission = schema.ASCIILine(
        title=u"Read Permission",
        description=u"If the user does not have this permission this field "
            "will not appear in write views",
        required=False
    )
    '''

