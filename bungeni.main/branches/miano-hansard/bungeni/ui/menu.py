# encoding: utf-8
# Bungeni Parliamentary Information System - http://www.bungeni.org/
# Copyright (C) 2010 - Africa i-Parliaments - http://www.parliaments.info/
# Licensed under GNU GPL v2 - http://www.gnu.org/licenses/gpl-2.0.txt
from __future__ import with_statement
"""Setup for some bungeni menus

$Id$
"""

log = __import__("logging").getLogger("bungeni.ui.menu")

import os
import operator
import datetime
from lxml import etree
import base64

from zope import component
from zope.app.component.hooks import getSite
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.browsermenu.interfaces import IBrowserMenu
import zope.browsermenu
from zope.security import proxy, checkPermission
from zope.i18n import translate
import z3c.menu.ready2go.item

from bungeni.core.workflow.interfaces import IWorkflow, IWorkflowController

from bungeni.alchemist.interfaces import IAlchemistContainer
from bungeni.models.utils import get_db_user_id
from bungeni.models.interfaces import IVersion, IScheduleText, IBungeniContent

from bungeni.core.translation import (get_language, get_all_languages, 
    get_available_translations, translate_i18n
)
from bungeni.core.dc import IDCDescriptiveProperties
from bungeni.core import schedule

from bungeni.ui.i18n import  _
from bungeni.ui.utils import url, misc
from bungeni.ui import interfaces

from bungeni.utils.capi import capi


class BrowserMenu(zope.browsermenu.menu.BrowserMenu):
    pass


class BrowserSubMenuItem(zope.browsermenu.menu.BrowserSubMenuItem):
    @property
    def id(self):
        return self.submenuId


def get_actions(name, context, request):
    menu = component.getUtility(IBrowserMenu, name)
    items = menu.getMenuItems(context, request)

    site_url = url.absoluteURL(getSite(), request)
    _url = url.absoluteURL(context, request)

    for item in items:
        item["url"] = url.urljoin(_url, item["action"])
        item["id"] = item["title"].lower().replace(" ", "-")
        item["icon"] = url.urljoin(site_url, item["icon"])
    return items


class GlobalMenuItem(z3c.menu.ready2go.item.GlobalMenuItem):
    pass


class LoginAction(GlobalMenuItem):

    @property
    def available(self):
        available = IUnauthenticatedPrincipal.providedBy(
            self.request.principal)
        return available

    @property
    def title(self):
        return _("Login")


class LogoutAction(GlobalMenuItem):

    @property
    def available(self):
        authenticated = not IUnauthenticatedPrincipal. \
            providedBy(self.request.principal)
        return authenticated

    @property
    def title(self):
        return _("Logout")


class DashboardAction(GlobalMenuItem):

    @property
    def id(self):
        return "user-id"

    @property
    def title(self):
        return self.request.principal.id

    @property
    def available(self):
        authenticated = not IUnauthenticatedPrincipal. \
            providedBy(self.request.principal)
        return authenticated


class AdminAction(GlobalMenuItem):

    def getURLContext(self):
        site = getSite()
        return site["admin"]

    #@property
    #def available(self):
    #    context = self.getURLContext()
    #    return getInteraction().checkPermission("zope.ManageSite", context)


#
# class TaskMenu(managr.MenuManager):
#
#     def update(self):
#         """See zope.contentprovider.interfaces.IContentProvider"""
#         self.__updated = True
#
#         viewlets = self._getViewlets()
#
#         viewlets = self.filter(viewlets)
#         viewlets = self.sort(viewlets)
#         # Just use the viewlets from now on
#         self.viewlets=[]
#         for name, viewlet in viewlets:
#             if ILocation.providedBy(viewlet):
#                 viewlet.__name__ = name
#             self.viewlets.append(viewlet)
#         self._updateViewlets()
#
#     def _getViewlets(self):
#         interaction = getInteraction()
#         # Find all content providers for the region
#         viewlets = component.getAdapters(
#             (self.context, self.request, self.__parent__, self),
#             interfaces.IViewlet)


class TranslationSubMenuItem(BrowserSubMenuItem):
    # Note:
    # BrowserSubMenuItem is a BrowserView but BrowserMenu is just an object.

    title = _(u"label_translate", default=u"Language:")
    submenuId = "context_translate"
    order = 50

    #def __init__(self, context, request):
    #    super(TranslationSubMenuItem, self).__init__(context, request)

    @property
    def extra(self):
        language = get_language(self.context)
        return {
            "id": self.id,
            "class": "language-%s" % language,
            "state": language,
            "stateTitle": language
        }

    @property
    def description(self):
        return u""

    @property
    def action(self):
        _url = url.absoluteURL(self.context, self.request)
        if checkPermission("bungeni.translation.Add", self.context):
            return "%s/translate" % _url
        else:
            return _url

    def selected(self):
        return False


class TranslateMenu(BrowserMenu):
    @property
    def current_language(self):
        return "en"

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        _url = url.absoluteURL(context, request)
        if checkPermission("bungeni.translation.Add", context):
            language = get_language(context)
            available = get_available_translations(context)
            results = []
            for name, obj in get_all_languages().items():
                title = obj["name"]
                # skip the current language
                if name == language:
                    continue
                action_url = "%s/translate?language=%s" % (_url, name)
                extra = {
                    "id": "translation-action-%s" % name,
                    "separator": None,
                    "class": ""
                }
                translation_id = available.get(name)
                results.append(
                    dict(title=title,
                         description="",
                         action=action_url,
                         selected=translation_id is not None,
                         icon=None,
                         extra=extra,
                         submenu=None))
            return results
        else:
            return None

class WorkflowSubMenuItem(BrowserSubMenuItem):
    title = _(u"label_state", default=u"State:")
    submenuId = "context_workflow"
    order = 40

    def __new__(cls, context, request):
        # this is currently the only way to make sure this menu only
        # "adapts" to a workflowed context; the idea is that the
        # component lookup will fail, which will propagate back to the
        # original lookup request
        workflow = IWorkflow(context, None)
        if workflow is None:
            return
        return object.__new__(cls, context, request)

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context = context
        self.url = url.absoluteURL(context, request)
        self.request = request

    @property
    def extra(self):
        wfc = IWorkflowController(self.context, None)
        if wfc is None:
            return {"id": self.id}
        status = wfc.state_controller.get_status()
        stateTitle = translate(
            str(wfc.workflow.get_state(status).title),
            domain="bungeni",
            context=self.request)
        return {
            "id": self.id,
            "class": "state-%s" % status,
            "state": status,
            "stateTitle": stateTitle
        }

    @property
    def description(self):
        return u""

    @property
    def action(self):
        return self.url

    def selected(self):
        return False


class WorkflowMenu(BrowserMenu):
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form.
        !+TAL-friendly(mr, sep-2011) means what?
        """
        if (not interfaces.IWorkspaceOrAdminSectionLayer.providedBy(request) or
                interfaces.IFormEditLayer.providedBy(request) or
                IVersion.providedBy(context)
            ):
            return ()
        #!+wfc.workflow
        wf = IWorkflow(context, None)
        if wf is None:
            return ()
        #state = IWorkflowController(context).state_controller.get_status()
        wfc = IWorkflowController(context)
        wf = wfc.workflow
        tids = wfc.getManualTransitionIds()
        
        _url = url.absoluteURL(context, request)
        results = []
        for tid in tids:
            transit_url = \
                "%s/change_workflow_state?transition_id=%s&next_url=..." % (
                    _url, tid)
            extra = {"id": "workflow-transition-%s" % tid,
                     "separator": None,
                     "class": ""}
            state_title = translate(str(wf.get_transition(tid).title),
                domain="bungeni",
                context=request)
            results.append(
                dict(title=state_title,
                     description="",
                     action=transit_url,
                     selected=False,
                     transition_id=tid,
                     icon=None,
                     extra=extra,
                     submenu=None))
        return results


class CalendarSubMenuItem(BrowserSubMenuItem):
    title = _(u"label_calendar_context", default=u"Calendar:")
    submenuId = "context_calendar"
    order = 10

    def __new__(cls, context, request):
        if context.get_group() is not None:
            return object.__new__(cls, context, request)

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context = context
        self.url = url.absoluteURL(context, request)

    @property
    def extra(self):
        return {
            "id": self.id,
            "stateTitle": self.context.label
        }

    @property
    def description(self):
        return u""

    @property
    def action(self):
        return self.url

    def selected(self):
        return False

class CalendarMenu(BrowserMenu):
    """Retrieve menu actions for available calendars."""

    def getSchedulingContexts(self, request):
        """Set up scheduling contexts.

        Currently we include:

        - committees
        - plenary

        """

        contexts = []
        app = getSite()
        today = datetime.date.today()
        if interfaces.IWorkspaceSchedulingSectionLayer.providedBy(request):
            committees = app["workspace"]["scheduling"]["committees"].values()
        else:
            committees = app["business"]["committees"].values()

        user_id = get_db_user_id()
        for committee in committees:
            if user_id:
                if ((committee.end_date is None
                     or committee.end_date >= today) and
                   (committee.start_date is None
                    or committee.start_date <= today) and
                   checkPermission("bungeni.agendaitem.Add", committee) and
                   (committee.status == "active")):
                    contexts.append(schedule.CommitteeSchedulingContext(
                            committee))
            else:
                if ((committee.end_date is None
                     or committee.end_date >= today) and
                   (committee.start_date is None
                    or committee.start_date <= today) and
                   (committee.status == "active")):
                    contexts.append(schedule.CommitteeSchedulingContext(
                            committee))
        for context in contexts:
            context.__name__ = u"schedule"
        if interfaces.IWorkspaceSchedulingSectionLayer.providedBy(request):
            contexts.append(schedule.ISchedulingContext(
                    app["workspace"]["scheduling"]))
        else:
            contexts.append(schedule.ISchedulingContext(
                    app["business"]["sittings"]))
        contexts[-1].__name__ = u""
        return contexts

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        group_id = context.get_group().group_id
        contexts = self.getSchedulingContexts(request)
        results = []
        for context in contexts:
            group = context.get_group()
            if group.group_id == group_id:
                continue
            _url = url.absoluteURL(context, request)
            extra = {
                # !+HTML_ID(mario, may-2011) what is the use of making the
                # (presumably HTML, used for styling... ) id be derived from
                # an sql surrogate pk ?!
                "id": "calendar-link-%s" % group.group_id,
                "separator": None,
                "class": ""
            }
            #!+(miano. nov-2010) description is set to be the same as title
            # below because the description of a group is a rich text field
            # that may have HTML formatting etc thus is not suitable to be
            # used as a tootip
            results.append(dict(
                    title=context.label,
                    description=context.label,
                    action=_url,
                    selected=False,
                    icon=None,
                    extra=extra,
                    submenu=None
            ))

        # sort on title
        results.sort(key=operator.itemgetter("title"))
        return results

class DownloadDocumentSubMenuItem(BrowserSubMenuItem):
    title = _(u"label_document_download", default=u"download document")
    submenuId = "context_download_document"
    order = 8
    
    def __new__(cls, context, request):
        """if IAlchemistContainer.providedBy(context):
            unproxied = proxy.removeSecurityProxy(context)
            if not IBungeniContent.implementedBy(unproxied.domain_model):
                return
        elif not IBungeniContent.providedBy(context):
            return
        """
        return object.__new__(cls, context, request)

    @property
    def extra(self):
        return {}
    
    @property
    def description(self):
        return ""
    
    @property
    def action(self):
        return url.absoluteURL(self.context, self.request)
    
    def selected(self):
        return False

i18n_pdf = _(u"Download PDF")
i18n_odt = _(u"Download ODT")
i18n_akomantoso = _(u"Akoma Ntoso")
i18n_rss = _(u"RSS")

class DownloadDocumentMenu(BrowserMenu):

    def documentTemplates(self):
        templates = []
        templates_path = capi.get_path_for("reporting", "templates", 
            "templates.xml"
        )
        if os.path.exists(templates_path):
            template_config = etree.fromstring(open(templates_path).read())
            for template in template_config.iter(tag="template"):
                location = capi.get_path_for("reporting", "templates", 
                    template.get("file")
                )
                template_file_name = template.get("file")
                if os.path.exists(location):
                    template_dict = dict(
                        title = template.get("name"),
                        language = template.get("language"),
                        location = base64.encodestring(template_file_name)
                    )
                    templates.append(template_dict)
                else:
                    log.error("Template does not exist. No file found at %s.", 
                        location
                    )
        return templates

    def getMenuItems(self, context, request):
        results = []
        _url = url.absoluteURL(context, request)
        if IBungeniContent.providedBy(context):
            doc_templates = self.documentTemplates()
            for doc_type in ["pdf", "odt"]:
                if doc_templates:
                    for template in doc_templates:
                        i18n_title = translate_i18n(globals()["i18n_%s" % doc_type])
                        results.append(dict(
                            title="%s [%s]" % (i18n_title,template.get("title")),
                            description="",
                            action="%s/%s?template=%s" % (_url, doc_type, 
                                template.get("location")),
                            selected=False,
                            extra = {
                                "id": "download-%s-%s" %(doc_type,
                                    misc.slugify(template.get("location"))
                                ),
                                "class": "download-document"
                            },
                            icon=None,
                            submenu=None
                        ))
                    
                else:
                    results.append(dict(
                        title = doc_type,
                        description=doc_type,
                        action = "%s/%s" %(_url, doc_type),
                        selected=False,
                        icon=None,
                        extra={},
                        submenu=None
                    ))
        if interfaces.IRSSRepresentationLayer.providedBy(request):
            for doc_type in ["akomantoso", "rss"]:
                results.append(dict(
                        title = globals()["i18n_%s" % doc_type],
                        description="",
                        action = "%s/feed.%s" %(_url, doc_type),
                        selected=False,
                        icon=None,
                        extra={
                            "id": "download-%s" % doc_type
                        },
                        submenu=None
                ))
        return results
        
class CalendarContentSubMenuItem(CalendarSubMenuItem):
    title = _(u"label_calendar_content_manager", default=u"Manage:")
    submenuId = "calendar_content_manager"
    order = 10
    
    @property
    def extra(self):
        return {
            "id": self.id,
            "stateTitle": _("Manage Scheduling Content")
        }

class CalendarContentMenu(BrowserMenu):
    """Generate menu items within scheduling to access calendar content manager.
    
    Allows adding of items such as headings for reuse within scheduling contexts
    """
    def getMenuItems(self, context, request):
        results = []
        try:
            items = proxy.removeSecurityProxy(context.__parent__).items()
        except AttributeError:
            return results
        for key, item in items:
            if not IAlchemistContainer.providedBy(item): continue
            if not IScheduleText.implementedBy(item.domain_model): continue
            dc_adapter = IDCDescriptiveProperties(item, None)
            if dc_adapter:
                _title = dc_adapter.title
            else:
                _title = getattr(item, "title", "Unknown")
            results.append(dict(
                title=_title,
                description=_title,
                action = url.absoluteURL(item, request),
                selected=False,
                icon=None,
                extra={},
                submenu=None
                
            ))
        return results
