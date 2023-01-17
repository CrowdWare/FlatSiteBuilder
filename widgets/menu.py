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

from widgets.menuitem import Menuitem
from PySide6.QtCore import QObject, Property, ClassInfo
from PySide6.QtQml import ListProperty


@ClassInfo(DefaultProperty = 'items')
class Menu(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.id = 0
        self._name = ""
        self._items = []

    def setId(self, id):
        self.id = id

    def item(self, n):
        return self._items[n]

    def itemCount(self):
        return len(self._items)

    def appendItem(self, item):
        self._items.append(item)

    items = ListProperty(Menuitem, appendItem)

    @Property('QString')
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def addMenuitem(self, item):
        self._items.append(item)

    def removeItem(self, item):
        self._items.remove(item)
