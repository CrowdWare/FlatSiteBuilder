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
from widgets.row import Row
from widgets.item import Item

@ClassInfo(DefaultProperty = 'items')
class Section(Item):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._fullwidth = False
        self._cssclass = ""
        self._style = ""
        self._attributes = ""
        self._id = ""
        self._items = []

    def item(self, n):
        return self._items[n]

    def itemCount(self):
        return len(self._items)

    def appendItem(self, item):
        self._items.append(item)

    items = ListProperty(Item, appendItem)

    @Property('bool')
    def fullwidth(self):
        return self._fullwidth

    @fullwidth.setter
    def fullwidth(self, fullwidth):
        self._fullwidth = fullwidth

    @Property('QString')
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @Property('QString')
    def cssclass(self):
        return self._cssclass

    @cssclass.setter
    def cssclass(self, cssclass):
        self._cssclass = cssclass

    @Property('QString')
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = style

    @Property('QString')
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    def clone(self):
        sec = Section()
        sec.fullwidth = self._fullwidth
        sec.cssclass = self._cssclass
        sec.style = self._style
        for item in self._items:
            sec._items.append(item.clone())
        return sec

    def getQml(self, indent):
        qml = "\n"
        qml += " " * indent + "Section {\n"
        qml += self.getAttributeQml(indent + 4, "id", self._id)
        qml += self.getAttributeQml(indent + 4, "cssclass", self._cssclass)
        qml += self.getAttributeQml(indent + 4, "style", self._style)
        qml += self.getAttributeQml(indent + 4, "attributes", self._attributes)
        qml += self.getAttributeQml(indent + 4, "fullwidth", self._fullwidth)
        for item in self._items:
            qml += item.getQml(indent + 4)
        qml += " " * indent + "}\n"
        return qml

    def collectTagNames(self, list):
        for item in self._items:
            if isinstance(item, Row):
                item.collectTagNames(list)
            else:
                if not item.tag_name in list:
                    list.append(item.tag_name)

    def getHtml(self):
        html = ""
        if self.fullwidth:
            for item in self._items:
                html += item.getHtml() + "\n"
        else:
            html += "<section"
            if self._cssclass:
                cssclass = self._cssclass
            else:
                cssclass = "container"
            html += " class=\"" + cssclass + "\""
            if self._id:
                html += " id=\"" + self._id +"\""
            if self._style:
                html += " style=\"" + self._style + "\""
            if self._attributes:
                html += " " + self._attributes
            html += ">\n"
            for item in self._items:
                html += item.getHtml()
            html += "</section>\n"
        return html

    def insertElement(self, sec, new_pos):
        self._items.insert(new_pos, sec)