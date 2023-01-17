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
from widgets.column import Column
from widgets.item import Item


@ClassInfo(DefaultProperty = 'columns')
class Row(Item):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._columns = []
        self._cssclass = ""
        
    def item(self, n):
        return self._columns[n]

    def itemCount(self):
        return len(self._columns)

    def appendItem(self, item):
        self._columns.append(item)

    columns = ListProperty(Column, appendItem)

    @Property('QString')
    def cssclass(self):
        return self._cssclass

    @cssclass.setter
    def cssclass(self, cssclass):
        self._cssclass = cssclass

    def clone(self):
        row = Row()
        row.cssclass = self._cssclass
        for column in self._columns:
            row._columns.append(column.clone())
        return row

    def getQml(self, indent):
        qml = "\n"
        qml += " " * indent + "Row {\n"
        qml += self.getAttributeQml(indent + 4, "cssclass", self.cssclass)
        for item in self._columns:
            qml += item.getQml(indent + 4)
        qml += " " * indent + "}\n"
        return qml

    def getHtml(self):
        html = "<div class=\"row"
        if self._cssclass:
            html += " " + self._cssclass
        html += "\">\n"
        for item in self._columns:
            html += item.getHtml()
        return html + "</div>\n"

    def collectTagNames(self, list):
        for item in self._columns:
            item.collectTagNames(list)

    def addColumn(self, column):
        self._columns.append(column)
