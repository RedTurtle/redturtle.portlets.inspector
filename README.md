redturtle.portlets.inspector
============================

redturtle.portlets.inspector is a report view to check the portlets inside a
Plone site.

The report view
---------------
This product gives you a view called `@@inspect-portlets`.
To visit this view you have to be manager.

You can call it on the root of your Plone site, e.g.:
 - http://localhost:8080/Plone-site-id/@@inspect-portlets
or in restrict your analysis in a subsection of your site, e.g.:
 - http://localhost:8080/Plone-site-id/sub/section/@@inspect-portlets

For a newly created Plone site it will output:
```
{'/Plone': {u'plone.leftcolumn': [<class 'plone.app.portlets.portlets.navigation.Assignment'>],
            u'plone.rightcolumn': [<class 'plone.app.portlets.portlets.news.Assignment'>,
                                   <class 'plone.app.portlets.portlets.events.Assignment'>]}}
```

Installation
------------
Just add this egg to your instance eggs.
```
eggs+=
    redturtle.portlets.inspector
```

If your are using an older version of Plone (before 3.3), you will also have
to add this egg to the zcml.
```
zcml+=
    redturtle.portlets.inspector
```

Why you want it
---------------
You may want to check this view for several reasons:
 - you want to remove a product that provides a portlet and want to remove all 
   the related portlets in your site otherwise it will break
 - you want to analyze a Plone site before migrating it
 - you are simply curious