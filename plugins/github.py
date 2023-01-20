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
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FlatSiteBuilder.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from PySide6.QtWidgets import QApplication, QWidget, QTextBrowser, QGridLayout, QPushButton, QLabel, QLineEdit
from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QFile, QCoreApplication, QSettings
from widgets.interfaces import PublisherInterface
from dulwich.repo import Repo
from dulwich.objects import Commit
from dulwich import porcelain
import shutil
import os
import plugins.github_rc

class GithubPublisher(PublisherInterface):
    def __init__(self):
        QWidget.__init__(self)
        publish = QPushButton("Push")
        publish.clicked.connect(self.push)
        caption = QLabel("Github Publisher")
        self.userid = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.reponame = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.display_name = "GithubPublisher"
        self.html = ""
        self.browser = QTextBrowser()
        self.browser.setHtml(self.html)
        self.image = QLabel()
        self.image.setPixmap(QPixmap.fromImage(QImage(":/github.png")))
        layout = QGridLayout()
        layout.addWidget(self.image, 0, 0, 1, 2)
        layout.addWidget(caption, 1, 0)
        layout.addWidget(QLabel("Organisation"), 2, 0)
        layout.addWidget(self.username, 2, 1)
        layout.addWidget(QLabel("Repository"), 3, 0)
        layout.addWidget(self.reponame, 3, 1)
        layout.addWidget(QLabel("User Id"), 4, 0)
        layout.addWidget(self.userid, 4, 1)
        layout.addWidget(QLabel("Password"), 5, 0)
        layout.addWidget(self.password, 5, 1)
        layout.addWidget(self.browser, 6, 0, 1, 2)
        layout.addWidget(publish)
        self.setLayout(layout)
        self.site_path = ""


        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        self.userid.setText(settings.value("github.userid"))
        self.username.setText(settings.value("github.username"))
        self.reponame.setText(settings.value("github.reponame"))


    def setSitePath(self, site_path, project_path):
        self.site_path = site_path

    def push(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        username = self.username.text()
        userid = self.userid.text()
        password = self.password.text()
        reponame = self.reponame.text()
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, QCoreApplication.organizationName(), QCoreApplication.applicationName())
        settings.setValue("github.userid", userid)
        settings.setValue("github.username", username)
        settings.setValue("github.reponame", reponame)
        os.chdir(self.site_path)

        gitpath = os.path.join(self.site_path, ".git")
        if os.path.exists(gitpath):
            repo = porcelain.open_repo(self.site_path)
        else:
            repo = porcelain.init(self.site_path)
        for r, dirs, files in os.walk(self.site_path):
            for f in files:
                p = os.path.join(r, f)[len(self.site_path) + 1:]
                if not ".git" in p:
                    porcelain.add(repo, p)
                    self.html = "<p>adding: " + p + "</p>" + self.html
                    self.browser.setHtml(self.html)
                    QCoreApplication.processEvents()
        self.html = "<p>Commiting changes</p>" + self.html
        self.browser.setHtml(self.html)
        QCoreApplication.processEvents()
        porcelain.commit(repo, b"A sample commit")
        
        self.html = "<p>Pushing to server</p>" + self.html
        self.browser.setHtml(self.html)
        QCoreApplication.processEvents()

        porcelain.push(self.site_path, "https://" + userid + ":" + password + "@github.com/" + username + "/" + reponame + ".git", "master")
        
        self.html = "<p>Ready</p>" + self.html
        self.browser.setHtml(self.html)
        QCoreApplication.processEvents()

        QApplication.restoreOverrideCursor()