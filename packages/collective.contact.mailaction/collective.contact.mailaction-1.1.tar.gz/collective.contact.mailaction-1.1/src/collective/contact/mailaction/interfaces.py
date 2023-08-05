# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveContactMailactionLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveContactMailactionTemplate(Interface):
    """Marker interface that defines a Mail Template."""
