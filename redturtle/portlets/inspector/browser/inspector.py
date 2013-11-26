# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Products.Five import BrowserView
from cStringIO import StringIO
from plone.app.portlets.interfaces import IPortletManager
from plone.memoize.view import memoize
from pprint import PrettyPrinter
from zope.component import getMultiAdapter, getUtilitiesFor

_marker = []


def shasattr(obj, attr):
    """ shasattr implementation inspired by Products.Archetypes

    https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/utils.py  # noqa
    """
    return getattr(aq_base(obj), attr, _marker) is not _marker


class InspectPortlets(BrowserView):
    '''
    Base view to inspect portlets
    '''
    @property
    @memoize
    def portlet_managers(self):
        ''' Returns the portlet managers, e.g.:
         - plone.leftcolumn
         - plone.rightcolumn
         - ...
        '''
        managers = getUtilitiesFor(IPortletManager)
        return tuple(managers)

    def assignments(self, obj):
        '''
        Get assignments for object, i.e. the portlets assigned in the context
        of obj
        '''
        all_assignments = {}
        for manager_name, manager in self.portlet_managers:
            manager_assignments = getMultiAdapter((obj, manager))
            try:
                keys = manager_assignments.keys()
            except AttributeError:
                keys = []
            if keys:
                values = [
                    (repr(manager_assignments[x]),
                     repr(manager_assignments[x].__class__))
                    for x in keys
                    if manager_assignments[x]
                ]
                if values:
                    all_assignments[manager_name] = values
        return all_assignments

    def update_results(self, obj):
        '''
        Update the results
        '''
        assignments = self.assignments(obj)
        if assignments:
            self.results['/'.join(obj.getPhysicalPath())] = assignments
        if shasattr(obj, 'listFolderContents'):
            for x in obj.listFolderContents():
                self.update_results(x)

    def __call__(self):
        '''
        Check the portlets defined here and in some sublevels
        '''
        self.results = {}
        self.update_results(self.context)
        printer = PrettyPrinter(stream=StringIO())
        printer.pprint(self.results)
        return printer._stream.getvalue()
