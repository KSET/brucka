# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'citajmi.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('django.contrib.*',),
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
        ))



        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            collapsible=False,
            column=2,
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=3,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
            ]
        ))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=3,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))
