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
import sys
from widgets.flatbutton import FlatButton
from widgets.generator import Generator
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QTextBrowser, QFileDialog
from PySide6.QtGui import QFont, QDesktopServices
from PySide6.QtCore import QUrl, Qt, Signal, Slot, QCoreApplication
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from widgets.plugins import Plugins
import resources


class Dashboard(QWidget):
    loadSite = Signal(str)
    createSite = Signal()
    buildSite = Signal()
    publishSite = Signal()
    previewSite = Signal()

    def __init__(self, site, default_path):
        QWidget.__init__(self)

        self.site = site
        if default_path:
            self.default_path = default_path
        else:
            self.default_path = os.path.join(Generator.install_directory, "sources")

        vbox = QVBoxLayout()
        layout = QGridLayout()
        title = QLabel()
        title.setText(QCoreApplication.translate("Dashboard", "Dashboard"))
        fnt = title.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        title.setFont(fnt)

        self.browser = QTextBrowser()
        self.browser.setOpenLinks(False)

        self.load_button = FlatButton(":/images/load_normal.png", ":/images/load_hover.png", ":/images/load_pressed.png")
        self.load_button.setToolTip(QCoreApplication.translate("Dashboard", "Load an existing website project"))

        self.create_button = FlatButton(":/images/create_normal.png", ":/images/create_hover.png", ":/images/create_pressed.png")
        self.create_button.setToolTip(QCoreApplication.translate("Dashboard", "Create a website project"))

        self.publish_button = FlatButton(":/images/publish_normal.png", ":/images/publish_hover.png", ":/images/publish_pressed.png")
        self.publish_button.setToolTip(QCoreApplication.translate("Dashboard", "Upload the website to your web space provider"))

        self.preview_button = FlatButton(":/images/preview_normal.png", ":/images/preview_hover.png", ":/images/preview_pressed.png")
        self.preview_button.setToolTip(QCoreApplication.translate("Dashboard", "Load the website in your browser locally"))

        self.build_button = FlatButton(":/images/build_normal.png", ":/images/build_hover.png", ":/images/build_pressed.png")
        self.build_button.setToolTip(QCoreApplication.translate("Dashboard", "Build the website"))

        self.info = QLabel()
        if self.site and self.site.title:
            self.info.setText(self.site.title + " " + QCoreApplication.translate("Dashboard", "loaded..."))
        else:
            self.info.setText(QCoreApplication.translate("Dashboard", "No site loaded yet..."))

        space = QWidget()
        space2 = QWidget()
        space3 = QWidget()
        space.setMinimumHeight(30)
        space2.setMinimumHeight(30)
        space3.setMinimumHeight(30)
        layout.addWidget(title, 0, 0, 1, 3)
        layout.addWidget(self.info, 1, 0, 1, 3)
        layout.addWidget(space, 2, 0)
        layout.addWidget(self.load_button, 3, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.create_button, 3, 1, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.publish_button, 3, 2, 1, 1, Qt.AlignCenter)
        layout.addWidget(space2, 4, 0)
        layout.addWidget(self.preview_button, 5, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.build_button, 5, 1, 1, 1, Qt.AlignCenter)

        #load generator plugins here
        
        for plugin_name in Plugins.generatorPluginNames():
            p = Plugins.getGeneratorPlugin(plugin_name)
            button = FlatButton(os.path.join(Plugins.getBundleDir(), "plugins",p.normal_image), os.path.join(Plugins.getBundleDir(), "plugins",p.hover_image), os.path.join(Plugins.getBundleDir(), "plugins",p.pressed_image))
            button.setToolTip(QCoreApplication.translate("Dashboard", "Execute Plugin"))
            button.clicked.connect(p.clicked)
            layout.addWidget(button, 5, 2, 1, 1, Qt.AlignCenter)

        vbox.addLayout(layout)
        vbox.addSpacing(40)
        vbox.addWidget(self.browser)
        self.setLayout(vbox)

        self.load_button.clicked.connect(self.loadClicked)
        self.create_button.clicked.connect(self.createClicked)
        self.publish_button.clicked.connect(self.publishClicked)
        self.preview_button.clicked.connect(self.previewClicked)
        self.build_button.clicked.connect(self.buildClicked)

        manager = QNetworkAccessManager(self)
        manager.finished.connect(self.fileIsReady)
        manager.get(QNetworkRequest(QUrl("https://CrowdWare.github.io/FlatSiteBuilder/news.html")))

    @Slot(QNetworkReply)
    def fileIsReady(self, reply):
        self.browser.setHtml(str(reply.readAll(), encoding="utf-8"))
        self.browser.anchorClicked.connect(self.anchorClicked)

    @Slot(QUrl)
    def anchorClicked(self, url):
        QDesktopServices.openUrl(url)

    @Slot()
    def loadClicked(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("FlatSiteBuilder (*.qml);;All (*)")
        dialog.setWindowTitle("Load Site")
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(self.default_path)
        if dialog.exec_():
            fileName = dialog.selectedFiles()[0]
        del dialog
        if not fileName:
            return
        self.loadSite.emit(fileName)

    @Slot()
    def createClicked(self):
        self.createSite.emit()

    @Slot()
    def buildClicked(self):
        self.buildSite.emit()

    @Slot()
    def publishClicked(self):
        self.publishSite.emit()

    @Slot()
    def previewClicked(self):
        self.previewSite.emit()

    def siteLoaded(self, site):
        self.site = site
        if not self.site.title:
            self.info.setText("No site loaded yet...")
        else:
            self.info.setText(self.site.title + " loaded...")
