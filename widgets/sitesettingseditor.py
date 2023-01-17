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
import shutil
from widgets.undoableeditor import UndoableEditor
from widgets.plugins import Plugins
from widgets.generator import Generator
from widgets.imageselector import ImageSelector
from PySide6.QtWidgets import QLineEdit, QComboBox, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtGui import QImage
from PySide6.QtCore import QCoreApplication
import resources


class SiteSettingsEditor(UndoableEditor):
    def __init__(self, win, site):
        UndoableEditor.__init__(self)
        self.win = win
        self.site = site
        self.title = QLineEdit()
        self.titleLabel.setText(QCoreApplication.translate("SiteSettingsEditor", "Site Settings"))
        self.filename = site.source_path + "/" + site.filename
        self.description = QLineEdit()
        self.copyright = QLineEdit()
        self.keywords = QLineEdit()
        self.author = QLineEdit()
        self.output = QLineEdit()
        self.language = QLineEdit()
        self.logo = QLineEdit()
        seekButton = QPushButton("...")
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))
        self.copyright.setPlaceholderText("&copy 2019 your name")
        self.publisher = QComboBox()

        for key in Plugins.publishPluginNames():
            pi = Plugins.getPublishPlugin(key)
            if pi:
                self.publisher.addItem(pi.display_name, key)

        vbox = QVBoxLayout()
        vbox.addStretch()

        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Title")), 1, 0)
        self.layout.addWidget(self.title, 2, 0)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Description")), 3, 0)
        self.layout.addWidget(self.description, 4, 0, 1, 3)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Copyright")), 5, 0)
        self.layout.addWidget(self.copyright, 6, 0, 1, 3)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Keywords")), 7, 0)
        self.layout.addWidget(self.keywords, 8, 0, 1, 3)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Author")), 9, 0)
        self.layout.addWidget(self.author, 10, 0)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Output directory (relative to to source dir)")), 11, 0)
        self.layout.addWidget(self.output, 12, 0)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Language")), 13, 0)
        self.layout.addWidget(self.language, 14, 0)
        
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Logo")), 15, 0)
        self.layout.addWidget(self.logo, 16, 0)
        self.layout.addWidget(seekButton, 16, 1)
        self.layout.addWidget(self.image, 17, 0, 1, 2)
        self.layout.setRowStretch(17, 1)
        self.layout.addWidget(QLabel(QCoreApplication.translate("SiteSettingsEditor", "Plugin to be used for publishing")), 18, 0)
        self.layout.addWidget(self.publisher, 19, 0)
        self.layout.addLayout(vbox, 20, 0)

        self.load()

        self.title.editingFinished.connect(self.titleChanged)
        self.description.editingFinished.connect(self.descriptionChanged)
        self.copyright.editingFinished.connect(self.copyrightChanged)
        self.keywords.editingFinished.connect(self.keywordsChanged)
        self.author.editingFinished.connect(self.authorChanged)
        self.output.editingFinished.connect(self.outputChanged)
        self.language.editingFinished.connect(self.languageChanged)
        self.logo.editingFinished.connect(self.logoChanged)
        self.publisher.currentIndexChanged.connect(self.publisherChanged)
        seekButton.clicked.connect(self.seek)

    def seek(self):
        fileName = ""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter("Images (*.png *.gif *.jpg);;All (*)")
        dialog.setWindowTitle(QCoreApplication.translate("SiteSettingsEditor", "Load Image"))
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]
        del dialog
        if not fileName:
            return

        # copy file to assets dir
        name = os.path.basename(fileName).replace(" ", "_")
        path = os.path.join(self.site.source_path, "assets", "images", name)
        self.logo.setText(os.path.basename(path))
        shutil.copy(fileName, path)

        # also copy file to deploy dir for previews
        dpath = os.path.join(self.site.source_path, self.site.output, "assets", "images", name)
        shutil.copy(fileName, dpath)

        self.image.setImage(QImage(path))
        self.contentChanged("logo changed")

    def load(self):
        oldTitle = self.site.title
        self.title.setText(self.site.title)
        self.description.setText(self.site.description)
        self.copyright.setText(self.site.copyright)
        self.keywords.setText(self.site.keywords)
        self.author.setText(self.site.author)
        self.output.setText(self.site.output)
        self.language.setText(self.site.language)
        self.logo.setText(self.site.logo)
        if self.site.logo:
            self.image.setImage(QImage(os.path.join(self.site.source_path, "assets", "images", self.site.logo)))
        index = self.publisher.findData(self.site.publisher)
        self.publisher.setCurrentIndex(index)
        #if oldTitle != self.site.title:
        #    os.rename(Generator.sitesPath() + "/" + oldTitle, Generator.sitesPath() + "/" + self.site.title)
        #    print("renaming1: " + Generator.sitesPath() + "/" + oldTitle)
        #    self.win.statusBar().showMessage("Site settings have been loaded. Site should be rebuilded. Output path has been renamed to " + self.site.title())

    def save(self):
        if self.site.title != self.title.text():
            oldTitle = self.site.title
            self.site.title = self.title.text()
            self.site.save()
            #os.rename(Generator.sitesPath() + "/" + oldTitle, Generator.sitesPath() + "/" + self.site.title)
            self.win.statusBar().showMessage(QCoreApplication.translate("SiteSettingsEditor", "Site settings have been saved. Site should be rebuilded on the dashboard.") + " " + QCoreApplication.translate("SiteSettingsEditor", "Output path has been renamed to") + " " + self.title.text())
        else:
            self.site.author = self.author.text()
            self.site.output = self.output.text()
            self.site.language = self.language.text()
            self.site.copyright = self.copyright.text()
            self.site.description = self.description.text()
            self.site.keywords = self.keywords.text()
            self.site.publisher = self.publisher.currentData()
            if not self.site.publisher:
                self.site.publisher = ""
            Plugins.setActualPublishPlugin(self.site.publisher)
            self.site.logo = self.logo.text()
            self.site.save()
            self.win.statusBar().showMessage(QCoreApplication.translate("SiteSettingsEditor", "Site settings have been saved. Site should be rebuilded on the dashboard."))

    def publisherChanged(self, publisher):
        if self.site.publisher != publisher:
            self.contentChanged("publisher changed")

    def titleChanged(self):
        if self.site.title != self.title.text():
            self.contentChanged("title changed")

    def authorChanged(self):
        if self.site.author != self.author.text():
            self.contentChanged("author changed")

    def outputChanged(self):
        if self.site.output != self.output.text():
            self.contentChanged("output changed")

    def languageChanged(self):
        if self.site.language != self.language.text():
            self.contentChanged("language changed")

    def logoChanged(self):
        if self.site.logo != self.logo.text():
            self.contentChanged("logo changed")

    def descriptionChanged(self):
        if self.site.description != self.description.text():
            self.contentChanged("description changed")

    def copyrightChanged(self):
        if self.site.copyright != self.copyright.text():
            self.contentChanged("copyright changed")

    def keywordsChanged(self):
        if self.site.keywords != self.keywords.text():
            self.contentChanged("keywords changed")
