# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr
from Products.Five import BrowserView
from plone.app.portlets.interfaces import IPortletManager
from plone.memoize.view import memoize
from zope.component import getMultiAdapter, getUtilitiesFor
from pprint import PrettyPrinter
from cStringIO import StringIO


class InspectPortlets(BrowserView):
    '''
    Base view to inspect portlets
    '''
    @property
    @memoize
    def portlet_managers(self):
        managers = getUtilitiesFor(IPortletManager)
        return tuple(managers)

    def assignments(self, obj):
        '''
        Get assignments for object
        '''
        all_assignments = {}
        for manager_name, manager in self.portlet_managers:
            manager_assignments = getMultiAdapter((obj, manager))
            try:
                keys = manager_assignments.keys()
            except:
                keys = []
            if keys:
                all_assignments[manager_name] = [type(manager_assignments[x])
                                                 for x
                                                 in keys]
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
