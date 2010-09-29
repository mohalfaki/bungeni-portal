import logging

from zope import component
from zope.securitypolicy.interfaces import IRole
from Products.PluggableAuthService.interfaces.plugins import *
from bungeni.plonepas.install import install as install_plonepas
from Products.CMFCore.utils import getToolByName

member_indexhtml="""\
member_search=context.restrictedTraverse('membership_view')
return member_search()
"""

def setup_who_authentication(context):
    if context.readDataFile('marker.txt') is None:
        return

    portal = context.getSite()
    pas = portal.acl_users
    if getattr(pas, 'who', None) is not None:
        return
    
    pas.manage_addProduct['whoopass'].manage_addWhoPlugin('who')

    plugins = pas.plugins
    plugins.activatePlugin(IExtractionPlugin, 'who')
    plugins.activatePlugin(IAuthenticationPlugin, 'who')
    plugins.activatePlugin(IGroupsPlugin, 'who')
    plugins.activatePlugin(IPropertiesPlugin, 'who')
    plugins.activatePlugin(IRolesPlugin, 'who')

def setup_plonepas(context):
    if context.readDataFile('marker.txt') is None:
        return

    portal = context.getSite()
    return install_plonepas(portal)

def setup_z2_roles(context):
    if context.readDataFile('marker.txt') is None:
        return    
    portal = context.getSite()
    roles = list(portal.__ac_roles__)
    for name, role in component.getUtilitiesFor(IRole):
        if name not in roles:
            roles.append(name)
    roles.sort()
    portal.__ac_roles__ = tuple(roles)


def update_authenticated_users_group(context):
    if context.readDataFile('marker.txt') is None:
        return
    portal = context.getSite()
    groups_tool = portal.portal_groups
    group = groups_tool.getGroupById('AuthenticatedUsers')
    if 'Member' and 'bungeni.Anybody' and 'bungeni.Everybody' not in group.getRoles():
        roles = group.getRoles() + ['Member', 'bungeni.Anybody', 'bungeni.Everybody']
        groups_tool.editGroup(group.id, roles=roles, groups=())
        
    
def setup_group_workspaces(context):
    """Turn on workspace creation.
       Set Workspace container id to 'committees'
       Set group workspaces container type to folder
       Set group workspaces
       Create the group folder
       Turn off portal navigation for the groups folder.
    """

    if context.readDataFile('marker.txt') is None:
        return

    portal = context.getSite()
    if 'groups' not in portal.objectIds():
        gtool = getToolByName(portal, 'portal_groups')
        gtool.groupWorkspacesCreationFlag = 1
        gtool.setGroupWorkspacesFolder('groups', 'Groups')
        gtool.setGroupWorkspaceContainerType('Folder')
        gtool.setGroupWorkspaceType('Folder')
            
        # create groups folder (Folder)

        groups = portal[
            portal.invokeFactory(
                "Folder",
                id="groups")]

        # set default properties
        groups.setTitle("Groups")
        groups.setDescription("Group workspaces container.")
        groups._getWorkflowTool().doActionFor(groups, 'publish' '')
        groups.setExcludeFromNav(True)
        groups.update()
