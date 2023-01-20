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

import datetime
import os
from tempfile import NamedTemporaryFile
from widgets.content import ContentType, Content
from widgets.menu import Menu
from widgets.menuitem import Menuitem
from widgets.menus import Menus
from widgets.generator import Generator
from PySide6.QtCore import QFileInfo, QObject, Property, QUrl, QCoreApplication
from PySide6.QtQml import QQmlEngine, QQmlComponent


class Site(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = ""
        self.win = None
        self.source_path = ""
        self._publisher = ""
        self._copyright = ""
        self._keywords = ""
        self._description = ""
        self._author = ""
        self._theme = ""
        self._title = ""
        self._logo = ""
        self._output = ""
        self._language = ""
        self.attributes = {}
        self.pages = []
        self.posts = []
        self.menus = None

    @Property('QString')
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    @Property('QString')
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        self._output = output

    @Property('QString')
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    @Property('QString')
    def copyright(self):
        return self._copyright

    @copyright.setter
    def copyright(self, copyright):
        self._copyright = copyright

    @Property('QString')
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        self._keywords = keywords

    @Property('QString')
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @Property('QString')
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @Property('QString')
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @Property('QString')
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, theme):
        self._theme = theme

    @Property('QString')
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, logo):
        self._logo = logo

    def setFilename(self, filename):
        info = QFileInfo(filename)
        self.filename = info.fileName()
        self.source_path = info.path()

    def filename(self):
        return self.filename

    def setWindow(self, win):
        self.win = win

    def save(self):
        html = "import FlatSiteBuilder 2.0\n\n"
        html += "Site {\n"
        html += "   title: '" + self.title + "'\n"
        html += "   theme: '" + self.theme + "'\n"
        html += "   description: '" + self.description + "'\n"
        html += "   copyright: '" + self.copyright + "'\n"
        html += "   keywords: '" + self.keywords + "'\n"
        html += "   author: '" + self.author + "'\n"
        html += "   logo: '" + self.logo + "'\n"
        html += "   language: '" + self.language + "'\n"
        html += "   publisher: '" + self.publisher + "'\n"
        html += "   output: '" + self.output + "'\n"
        html += "}\n"
        with open(os.path.join(self.source_path, "Site.qml"), "w") as f:
            f.write(html)
        if self.win:
            self.win.statusBar().showMessage(QCoreApplication.translate("Site", "Site has been saved"))

    def saveMenus(self):
        html = "import FlatSiteBuilder 2.0\n\n"
        html += "Menus {\n"
        for i in range(self.menus.menuCount()):
            menu = self.menus.menu(i)
            html += "    Menu {\n"
            html += "        name: '" + menu.name + "'\n"
            for j in range(menu.itemCount()):
                item = menu.item(j)
                html += "        Menuitem {\n"
                html += "            title: '" + item.title + "'\n"
                html += "            url: '" + item.url + "'\n"
                html += "            icon: '" + item.icon + "'\n"
                html += "            attributes: '" + item.attributes + "'\n"
                for k in range(item.itemCount()):
                    subitem = item.item(k)
                    html += "            Menuitem {\n"
                    html += "                title: '" + subitem.title + "'\n"
                    html += "                url: '" + subitem.url + "'\n"
                    html += "                icon: '" + subitem.icon + "'\n"
                    html += "            }\n"
                html += "        }\n"
            html += "    }\n"
        html += "}\n"

        with open(os.path.join(self.source_path, "Menus.qml"), "w") as f:
            f.write(html)
        if self.win:
            self.win.statusBar().showMessage(QCoreApplication.translate("Site", "Menus have been saved"))
    
    def addMenu(self, menu):
        if not self.menus:
            self.menus = Menus()
        self.menus.appendMenu(menu)

    def loadMenus(self):
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.loadUrl(QUrl.fromLocalFile(os.path.join(self.source_path, "Menus.qml")))
        self.menus = component.create()
        if self.menus is not None:
            self.win.statusBar().showMessage(QCoreApplication.translate("Site", "Menus have been loaded"))
        else:
            for error in component.errors():
                print(error.toString())
        del engine

        # we have to loop through the menu items to set the parent for subitems
        if(self.menus == None):
            return
        for i in range(self.menus.menuCount()):
            menu = self.menus.menu(i)
            for j in range(menu.itemCount()):
                item = menu.item(j)
                for k in range(item.itemCount()):
                    subItem = item.item(k)
                    subItem.setParentItem(item)

    def removeMenu(self, menu):
        self.menus.remove(menu)

    def addAttribute(self, key, value):
        self.attributes[key] = value

    def addPage(self, page):
        self.pages.append(page)

    def loadPages(self):
        self.pages.clear()
        for root, dirs, files in os.walk(os.path.join(self.source_path, "pages")):
            for file in files:
                if file.endswith(".qml"):
                    page = self.loadContent(file, ContentType.PAGE)
                    self.pages.append(page)
        self.win.statusBar().showMessage(QCoreApplication.translate("Site", "Pages have been loaded"))

    def loadContent(self, source, type):
        if type == ContentType.PAGE:
            sub = "pages"
        else:
            sub = "posts"
        engine = QQmlEngine()
        component = QQmlComponent(engine)
        component.loadUrl(QUrl.fromLocalFile(os.path.join(self.source_path, sub, source)))
        content = component.create()
        if content is not None:
            content.source = source
            content.content_type = type
        else:
            for error in component.errors():
                print("site.loadContent", error.toString())
        return content

    def loadPosts(self):
        self.posts.clear()
        for root, dirs, files in os.walk(os.path.join(self.source_path, "posts")):
            for file in files:
                if file.endswith(".qml"):
                    post = self.loadContent(file, ContentType.POST)
                    self.posts.append(post)
        self.win.statusBar().showMessage(QCoreApplication.translate("Site", "Posts have been loaded"))


    def createTemporaryContent(self, type):
        temp = NamedTemporaryFile()
        name = os.path.basename(temp.name)
        if type == ContentType.PAGE:
            filename = os.path.join(self.source_path, "pages", name + ".qml")
        else:
            filename = os.path.join(self.source_path, "posts", name + ".qml")
        temp.close()

        content = Content()
        content.author = self.author
        content.keywords = self.keywords
        content.menu = "" #self.menus.menus[0]
        content.source = filename
        if type == ContentType.PAGE:
            content.layout = "default"
        else:
            content.layout = "post"
        content.date = datetime.datetime.now().strftime("%Y-%m-%d")
        content.save(filename)

        return filename 

