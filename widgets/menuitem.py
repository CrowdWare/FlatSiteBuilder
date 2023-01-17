#############################################################################
# Copyright (C) 2023 CrowdWare
#
# This file is part of FlatSiteBuilder.
#
#  FlatSiteBuilder is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FlatSiteBuilder is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PySide6.QtCore import QObject, Property, ClassInfo
from PySide6.QtQml import ListProperty


@ClassInfo(DefaultProperty = 'items')
class Menuitem(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._title = ""
        self._url = ""
        self._icon = ""
        #self._attr = ""
        self._attributes = ""
        #self.attributes = {}
        self._items = []
        self.parentItem = None


    def item(self, n):
        return self._items[n]

    def itemCount(self):
        return len(self._items)

    def appendItem(self, item):
        self._items.append(item)

    items = ListProperty(QObject, appendItem)

    @Property('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @Property('QString')
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @Property('QString')
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    @Property('QString')
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

 #   def addAttribute(self, key, value):
 #       self.attributes[key] = value

    def isSubitem(self):
        return self.parentItem != None

    def addMenuitem(self, item):
        self._items.append(item)
        item.setParentItem(self)

    def removeMenuitem(self, item):
        self._items.remove(item)
        item.setParentItem(None)

    def setParentItem(self, parent):
        self.parentItem = parent
