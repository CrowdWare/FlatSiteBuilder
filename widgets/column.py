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

from PySide6.QtCore import Property, QObject, ClassInfo
from PySide6.QtQml import ListProperty
from widgets.item import Item


@ClassInfo(DefaultProperty = 'items')
class Column(Item):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._items = []
        self._span = 0

    def item(self, n):
        return self._items[n]

    def itemCount(self):
        return len(self._items)

    def appendItem(self, item):
        self._items.append(item)

    items = ListProperty(Item, appendItem)

    @Property(int)
    def span(self):
        return self._span

    @span.setter
    def span(self, span):
        self._span = span

    def clone(self):
        col = Column()
        col.span = self._span
        for item in self._items:
            col._items.append(item.clone())
        return col

    def getQml(self, indent):
        qml = "\n"
        qml += " " * indent + "Column {\n"
        qml += self.getAttributeQml(indent + 4, "span", self._span)
        for item in self._items:
            qml += item.getQml(indent + 4)
        qml += " " * indent + "}\n"
        return qml

    def getHtml(self):
        html = "<div class=\"col-md-" + str(self._span) + "\">\n"
        for item in self._items:
            html += item.getHtml()
        return html + "\n</div>\n"

    def collectTagNames(self, list):
        for item in self._items:
            if not item.tag_name in list:
                list.append(item.tag_name)
    
    def insertElement(self, content, new_pos):
        self._items.insert(new_pos, content)

    def addItem(self, item):
        self._items.append(item)