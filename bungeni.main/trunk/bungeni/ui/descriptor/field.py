# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt

"""Support for UI Form Fields descriptions

$Id$
"""
log = __import__("logging").getLogger("bungeni.ui.descriptor.field")

from zope import schema
from bungeni.alchemist.model import ModelDescriptor, Field, show, hide
from bungeni.ui import widgets
from bungeni.ui.fields import VocabularyTextField
from bungeni.ui.i18n import _
from bungeni.ui.descriptor import listing, constraints


# supported value types
# {str: {property-kwarg:value}}
VALUETYPE = {
    "text": {},
    "date": {},
    "datetime": {},
    "bool": {"default": True},
    "number": {},
    "status": {},
    "language": {},
    "vocabulary": {}, # !+ constraint ?
    "email": {"constraint": constraints.check_email},
    "login": {"min_length": 3, "max_length": 20, "constraint": constraints.check_login},
    "password": {},
    "image": {},
    "file": {},
    "user": {},
    "member": {},
    "signatory": {}, # !+
    "combined_name": {}, # !+
}


# supported render types - determines the UI type for the field
# {str: zope.schema.Field} #!+kw:comma-separated-str
RENDERTYPE = {
    "text_line": schema.TextLine,
    "text_box": schema.Text,
    "rich_text": schema.Text,
    "date": schema.Date,
    "bool": schema.Bool,
    "number": schema.Int,
    "image": schema.Bytes,
    "file": schema.Bytes,
    # special other user-conf params: "vocabulary" -> "type:vocabulary, required:True"
    "single_select": schema.Choice, 
    "radio": schema.Choice, 
    "tree_text": VocabularyTextField,
    "no_input": None, # !+
}
RENDERTYPE_WITH_VOCABULARIES = ("single_select", "radio", "tree_text")


# widget setting per mode, by (value_type, render_type)
# (value, render): (view, edit, add, search, 
#   [listing_column_factory, listing_column_filter]) # !+delete
WIDGETS = {
    ("text", "text_line"):
        (None, None, None, None, 
            listing.truncatable_name_column, None),
    ("text", "text_box"):
        (None, widgets.TextAreaWidget, widgets.TextAreaWidget, None, 
            listing.truncatable_name_column, None),
    ("text", "rich_text"):
        (widgets.HTMLDisplay, widgets.RichTextEditor, widgets.RichTextEditor, 
            None, None, None),
    ("text", "radio"):
        (None, widgets.CustomRadioWidget, widgets.CustomRadioWidget, None, None, None),
    ("text", "single_select"):
        (None, None, None, None, None, None),
    ("text", "tree_text"):
        (widgets.TermsDisplayWidget, widgets.TreeVocabularyWidget, 
            widgets.TreeVocabularyWidget, None, None, None),
    ("text", "no_input"):
        (None, widgets.NoInputWidget, widgets.NoInputWidget, None, None, None),
    ("combined_name", "text_line"):
        (None, None, None, None, 
            listing.combined_name_column, 
            listing.combined_name_column_filter),
    ("date", "date"):
        (None, widgets.DateWidget, widgets.DateWidget, 
            widgets.date_input_search_widget,
            listing.date_column, None),
    ("datetime", "date"):
        (None, widgets.DateWidget, widgets.DateWidget, 
            widgets.date_input_search_widget,
            listing.datetime_column, None),
    ("bool", "bool"):
        (None, None, None, None, None, None),
    ("number", "number"):
        (None, None, None, None, None, None),
    ("status", "single_select"):
        (None, None, None, None, listing.workflow_column, None),
    ("language", "single_select"):
        (None, None, widgets.LanguageLookupWidget, None, None, None),
    ("vocabulary", "single_select"):
        (None, None, None, None, listing.vocabulary_column, None),
    ("email", "text_line"):
        (None, None, None, None, None, None),
    ("login", "text_line"):
        (None, None, None, None, None, None),
    ("password", "text_line"):
        (None, None, None, None, None, None),
    ("image", "image"):
        (widgets.ImageDisplayWidget, widgets.ImageInputWidget, None, None,
            None, None),
    ("file", "file"):
        (widgets.FileDisplayWidget, widgets.FileEditWidget, widgets.FileAddWidget, None,
            None, None),
    ("user", "no_input"): # !+User.user_id
        (None, None, None, None,
            listing.user_name_column,
            listing.user_listing_name_column_filter),
    ("user", "single_select"):
        (widgets.UserURLDisplayWidget, None, widgets.AutoCompleteWidget(), None,
            listing.related_user_name_column, 
            listing.related_user_name_column_filter),
    ("member", "single_select"): # !+combine with "user"
        (widgets.UserURLDisplayWidget, None, widgets.AutoCompleteWidget(), None,
            listing.linked_mp_name_column, 
            listing.related_user_name_column_filter),
    ("signatory", "no_input"): # !+Signatory.signatory_id
        (None, None, None, None,
            listing.simple_view_column, 
            None),
}


def F(name=None, label=None, description=None, 
        required=False, 
        #modes=None, #!+inferred from localizable
        localizable=None, #!+rename
        #property=None,
        #view_widget=None, edit_widget=None, add_widget=None, 
        #search_widget=None,
        #listing_column=None, 
        #listing_column_filter=None,
        value_type="text",
        render_type="text_line",
        vocabulary=None,
    ):
    """
    A "configuration layer" for Fields, to decouple lower level details from 
    Form UI configuration. Intention is to offer a simpler, more 
    "user-oriented" and "xml-friendly" way to declare a field.
    
    New parameters introduced by the F layer type:
        required, value_type, render_type, vocabulary
    that, when coupled with some additional application-level settings, 
    replace the following Field init parameters:
        modes
        property (along with own parameters)
        view_widget, edit_widget, add_widget, search_widget
        listing_column, listing_column_filter
    
    Example:
    
        F(name="language", label="Language", description=None, 
            required=True,
            localizable=[ show("view edit add"), hide("listing"), ]
            value_type="language",
            render_type="single_select",
            vocabulary="language_vocabulary"
        )
    
    will be the "user-oriented" equivalent way to define the following Field:
    
        Field(name="language",
            label=_("Language"),
            modes="view edit add listing",,
            localizable=[
                show("view edit"), 
                hide("listing"), 
            ]
            property=schema.Choice(title=_("Language"),
                vocabulary="language_vocabulary"
            ),
            add_widget=widgets.LanguageLookupWidget,
        )
    
    """
    # integrity
    if render_type in RENDERTYPE_WITH_VOCABULARIES:
        assert vocabulary, \
            "Vocabulary may not be None for render_type=%r" % (render_type)
    if vocabulary is not None:
        assert render_type in RENDERTYPE_WITH_VOCABULARIES, \
            "render_type=%r may not have a vocabulary [%r]" % (
                render_type, vocabulary)
    if value_type is not None:
        assert value_type in VALUETYPE, "Unknown value_type=%r" % (value_type)
    assert (value_type, render_type) in WIDGETS, \
        "No widget set defined for (value_type=%r, render_type=%r)" % (
            value_type, render_type)
    
    # i18n attributes
    if label:
        label = _(label)
    if description:
        description = _(description)
    
    # Field.*_widgets
    widgets = WIDGETS[(value_type, render_type)]

    # modes    
    if localizable is not None:
        # !+ ensure unique, normalized order
        modes = [ mode for loc in localizable for mode in loc.modes ]
    else:
        modes = []
    
    # listing column params
    listing_column, listing_column_filter = None, None
    if "listing" in modes:
        listing_column_factory = widgets[4]
        if listing_column_factory is not None:
            listing_column = listing_column_factory(name, label, vocabulary=vocabulary)
        listing_column_filter = widgets[5]
    
    # Field
    f = Field(name=name, 
            label=label, 
            description=description, 
            #modes=None
            localizable=localizable,
            listing_column=listing_column, 
            listing_column_filter=listing_column_filter,
        )
    
    # Field.property -- see zope.schema.Field, TextLine, Choice, ...
    if render_type is not None and RENDERTYPE[render_type] is not None:
        RType = RENDERTYPE[render_type]
        property_kwargs = dict(
            title=label,
            description=description,
            required=required
        )
        if vocabulary is not None:
            property_kwargs["vocabulary"] = vocabulary
        property_kwargs.update(VALUETYPE[value_type])
        f.property = RType(**property_kwargs)
    
    (f.view_widget, f.edit_widget, f.add_widget, f.search_widget
        ) = widgets[0:4]
        
    return f

