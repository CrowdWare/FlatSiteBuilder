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

import os
import datetime
from PySide6.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QComboBox, QGridLayout, QVBoxLayout
from PySide6.QtCore import Signal, QDir, QCoreApplication, Qt
from PySide6.QtGui import QPixmap, QPalette, QColor
import resources
from widgets.site import Site
from widgets.menu import Menu
from widgets.menuitem import Menuitem
from widgets.content import Content
from widgets.section import Section
from widgets.row import Row
from plugins.texteditor import Text
from widgets.column import Column
from widgets.content import ContentType

class SiteWizard(QWizard):
    loadSite = Signal(object)
    buildSite = Signal()

    def __init__(self, install_directory, parent = None):
        super(SiteWizard, self).__init__(parent)
        self.install_directory = install_directory
        self.addPage(IntroPage())
        self.addPage(SiteInfoPage(install_directory))
        self.addPage(ConclusionPage())
        self.setWindowTitle(QCoreApplication.translate("SiteWizard", "Site Wizard"))
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        
    def accept(self):
        siteName = self.field("siteName")
        description = self.field("description")
        copyright = self.field("copyright")
        theme = self.field("theme")

        path = os.path.join(self.install_directory, "sources", siteName.lower())
        os.mkdir(path)
        os.mkdir(os.path.join(path, "pages"))
        os.mkdir(os.path.join(path, "posts"))
        os.mkdir(os.path.join(path, "content"))
        os.mkdir(os.path.join(path, "includes"))
        os.mkdir(os.path.join(path, "layouts"))
        os.mkdir(os.path.join(path, "assets"))
        os.mkdir(os.path.join(path, "assets", "css"))
        os.mkdir(os.path.join(path, "assets", "fonts"))
        os.mkdir(os.path.join(path, "assets", "js"))
        os.mkdir(os.path.join(path, "assets", "images"))


        self.createSite(siteName, description, copyright, theme, path)
        
        super().accept()

        self.loadSite.emit(path + "/Site.qml")
        self.buildSite.emit()

    def createSite(self, siteName, description, copyright, theme, path):
        site = Site()
        site.theme = theme
        site.title = siteName
        site.output = "docs"
        if description:
            site.description = description
        if copyright:
            site.copyright = copyright
        site.source_path = path
        site.save()

        menu = Menu()
        menu.name = "default"
        item = Menuitem()
        item.title = "Index"
        item.url = "index.html"
        menu.addMenuitem(item)
        site.addMenu(menu)
        site.saveMenus()
        
        content = Content()
        content.title = "Index"
        content.menu = "default"
        content.author = "admin"
        content.layout = "default"
        content.content_type = ContentType.PAGE
        content.date = datetime.datetime.now().strftime("%Y-%m-%d")
        section = Section()
        row = Row()
        column = Column()
        column.span = 12
        text = Text()
        text.text = QCoreApplication.translate("SiteWizard", "<h1>Welcome</h1>\n<p>Todo...</p>")
        column.addItem(text)
        row.addColumn(column)
        section._items.append(row)
        content._items.append(section)
        content.save(os.path.join(path, "pages", "index.qml"))


class IntroPage(QWizardPage):

    def __init__(self):
        QWizardPage.__init__(self)
        self.setTitle(QCoreApplication.translate("SiteWizard", "Introduction"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/wizard.png"))

        label = QLabel(QCoreApplication.translate("SiteWizard", "This wizard will generate a skeleton website. "
                       "You simply need to specify the site name and set a "
                       "few options to produce the site."))
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class SiteInfoPage(QWizardPage):

    def __init__(self, install_directory):
        QWizardPage.__init__(self)
        self.install_directory = install_directory
        self.setTitle(QCoreApplication.translate("SiteWizard", "Site Information"))
        self.setSubTitle(QCoreApplication.translate("SiteWizard", "Specify basic information about the site for which you "
                         "want to generate site files."))
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/icon64.png"))

        self.siteNameLabel = QLabel(QCoreApplication.translate("SiteWizard", "&Site title:"))
        self.siteNameLineEdit = QLineEdit()
        self.siteNameLabel.setBuddy(self.siteNameLineEdit)
        self.siteNameLineEdit.setPlaceholderText(QCoreApplication.translate("SiteWizard", "Site title"))

        self.descriptionLabel = QLabel(QCoreApplication.translate("SiteWizard", "&Description:"))
        self.descriptionLineEdit = QLineEdit()
        self.descriptionLabel.setBuddy(self.descriptionLineEdit)
        self.descriptionLineEdit.setPlaceholderText(QCoreApplication.translate("SiteWizard", "Site description"))

        self.copyrightLabel = QLabel(QCoreApplication.translate("SiteWizard", "&Copyright"))
        self.copyrightLineEdit = QLineEdit()
        self.copyrightLabel.setBuddy(self.copyrightLineEdit)
        self.copyrightLineEdit.setPlaceholderText(QCoreApplication.translate("SiteWizard", "&copy 2022 YourCompany. All Rights Reserved."))

        self.themeLabel = QLabel(QCoreApplication.translate("SiteWizard", "&Theme"))
        self.theme = QComboBox()
        self.themeLabel.setBuddy(self.theme)

        themesDir = QDir(os.path.join(install_directory, "themes"))
        for theme in themesDir.entryList(QDir.NoDotAndDotDot | QDir.Dirs):
            self.theme.addItem(theme)

        self.registerField("siteName*", self.siteNameLineEdit)
        self.registerField("description", self.descriptionLineEdit)
        self.registerField("copyright", self.copyrightLineEdit)
        self.registerField("theme", self.theme, "currentText")

        self.warning = QLabel("")
        self.warning.setStyleSheet("QLabel  color : orange ")

        layout = QGridLayout()
        layout.addWidget(self.siteNameLabel, 0, 0)
        layout.addWidget(self.siteNameLineEdit, 0, 1)
        layout.addWidget(self.descriptionLabel, 1, 0)
        layout.addWidget(self.descriptionLineEdit, 1, 1)
        layout.addWidget(self.copyrightLabel, 2, 0)
        layout.addWidget(self.copyrightLineEdit, 2, 1)
        layout.addWidget(self.themeLabel, 3, 0)
        layout.addWidget(self.theme, 3, 1)
        layout.addWidget(self.warning, 4, 0, 1, 2)
        self.setLayout(layout)
        self.siteNameLineEdit.textChanged.connect(self.siteNameChanged)
        self.setAutoFillBackground(True)

    def siteNameChanged(self, name):
        if os.path.isdir(os.path.join(self.install_directory, "sources", name.lower())):
            self.warning.setText(QCoreApplication.translate("SiteWizard", "WARNING<br/>A site with the name") + " " + name.lower() + " " + QCoreApplication.translate("SiteWizard", "already exists.<br/>If you continue self site will be overridden."))
        else:
            self.warning.setText("")


class ConclusionPage(QWizardPage):

    def __init__(self):
        QWizardPage.__init__(self)
        self.setTitle(QCoreApplication.translate("SiteWizard", "Conclusion"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/wizard.png"))

        self.label = QLabel(QCoreApplication.translate("SiteWizard", "Click Finish to generate the site skeleton."))
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)