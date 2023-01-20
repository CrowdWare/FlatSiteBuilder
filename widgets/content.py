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

from PySide6.QtCore import Property, QObject, QDate, ClassInfo
from PySide6.QtGui import QPainter, QColor
from PySide6.QtQml import ListProperty
from enum import Enum
from widgets.section import Section
from widgets.item import Item
from widgets.plugins import Plugins


class ContentType(Enum):
    PAGE = 1
    POST = 2

@ClassInfo(DefaultProperty = 'items')
class Content(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._title = ""
        self._menu = "default"
        self._author = ""
        self._excerpt = ""
        self._keywords = ""
        self._script = ""
        self._layout = ""
        self._date = None
        self._logo = ""
        self._language = ""
        self.source = ""
        self.content_type = None
        self.attributes = {}
        self._items = []

    def item(self, n):
        return self._items[n]

    def itemCount(self):
        return len(self._items)

    def appendItem(self, item):
        self._items.append(item)

    items = ListProperty(Item, appendItem)

    @Property('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @Property('QString')
    def language(self):
        return self._language
    
    @language.setter
    def language(self, language):
        self._language = language

    @Property('QString')
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, logo):
        self._logo = logo

    @Property('QString')
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = layout

    @Property('QString')
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, menu):
        self._menu = menu

    @Property('QString')
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @Property('QString')
    def excerpt(self):
        return self._excerpt

    @excerpt.setter
    def excerpt(self, excerpt):
        self._excerpt = excerpt

    @Property('QString')
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @Property('QString')
    def script(self):
        return self._script

    @script.setter
    def script(self, script):
        self._script = script

    @Property('QDate')
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @Property('QString')
    def url(self):
        url = self.source
        return url.replace(".qml", ".html")

    def getAttributeQml(self, indent, att, value):
        qml = ""
        if value: 
            if isinstance(value, str):
                qml += " " * indent + att + ": \"" + value + "\"\n"
            elif isinstance(value, bool):
                qml += " " * indent + att + ": true\n"
            elif isinstance(value, QDate):
                qml +=" " * indent + att + ": \"" + value.toString("yyyy-MM-dd") + "\"\n"
        return qml

    def save(self, filename):
        qml = "import FlatSiteBuilder 2.0\n"
            
        taglist = []
        self.collectTagNames(taglist)

        for tag in taglist:
            plugin_name = Plugins.getElementPluginByTagname(tag)
            plugin = Plugins.element_plugins[plugin_name]
            qml += plugin.getImportString()
        qml += "\n"
        qml += "Content {\n"
        qml += self.getAttributeQml(4, "title", self.title)
        qml += self.getAttributeQml(4, "menu", self.menu)
        qml += self.getAttributeQml(4, "author", self.author)
        qml += self.getAttributeQml(4, "keywords", self.keywords)
        qml += self.getAttributeQml(4, "script", self.script)
        qml += self.getAttributeQml(4, "layout", self.layout)
        qml += self.getAttributeQml(4, "date", self.date)
        qml += self.getAttributeQml(4, "logo", self.logo)
        qml += self.getAttributeQml(4, "excerpt", self.excerpt)
        qml += self.getAttributeQml(4, "language", self.language)

        for att, value in self.attributes:
            qml += self.getAttributeQml(4, att, value) 
            
        for item in self._items:
            qml += item.getQml(4)

        qml += "}\n"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(qml)

    def changeSectionPos(self, sec, new_pos):
        self._items.remove(sec)
        self._items.insert(new_pos, sec)

    def appendSection(self, sec):
        self._items.append(sec)

    def removeSection(self, sec):
        self._items.remove(sec)

    def collectTagNames(self, list):
         for item in self._items:
             item.collectTagNames(list)
