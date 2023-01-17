#############################################################################
# Copyright (C) 2023 CrowdWare
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

from PySide6.QtWidgets import QWidget, QTextBrowser, QVBoxLayout
from PySide6 import QtCore
from PySide6.QtCore import QFile, QCoreApplication
from widgets.interfaces import PublisherInterface


class NoPublisher(PublisherInterface):
    def __init__(self):
        QWidget.__init__(self)
        self.display_name = "NoPublisher"
        self.browser = QTextBrowser()
        
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def setSitePath(self, fsb_path, project_path):
        html = \
        "<html>" \
        "<head>" \
        "</head>" \
        "<body style=\"margin:10; background-color: #353535; color: #ffffff;\">" \
        "<section class=\"container\">" \
        "<div class=\"row\">" \
        "<div class=\"col-md-12\">" \
        "<h1>No Publisher</h1>" \
        "<p>" + QCoreApplication.translate("NoPublisher", "This plugin is only here to demonstrate the possibility of a publisher plugin.") + "</p>" \
        "<p>" + QCoreApplication.translate("NoPublisher", "But you can publish your website manually using git with the following commands.") + "</p>" \
        "<p>&nbsp;</p>" \
        "<p>" + QCoreApplication.translate("NoPublisher", "Your content is stored at") + "<strong> " + project_path + "</strong></p>" \
        "<p>" + QCoreApplication.translate("NoPublisher", "Please exchange") + " <strong>mycompany</strong> " + QCoreApplication.translate("NoPublisher", "and") + " <strong>myproject</strong> " + QCoreApplication.translate("NoPublisher", "with the appropriate values.") + "</p>" \
        "<p>" + QCoreApplication.translate("NoPublisher", "We assume that you already have a github repository for your project. If not you should create a repo on github.com prior to push content.") + "</p>" \
        "<h3>" + QCoreApplication.translate("NoPublisher", "Publish site source") + "</h3>" \
        "<p style=\"font-family: Courier;\">" \
        "    <ul>" \
        "	    <li>cd " + project_path + "</li>" \
        "		<li>git init</li>" \
        "		<li>git add .</li>" \
        "		<li>git commit -m \"first commit\"</li>" \
        "		<li>git remote add origin https://github.com/mycompany/myproject.git</li>" \
        "		<li>git push -u origin master</li>" \
        "	</ul>" \
        "</p>" \
        "<h3>" + QCoreApplication.translate("NoPublisher", "Publish site content") + "</h3>" \
        "<p style=\"font-family: Courier;\">" \
        "    <ul>" \
        "	    <li>cd " + project_path + "</li>" \
        "		<li>git init</li>" \
        "		<li>git checkout --orphan gh-pages</li>" \
        "		<li>git add .</li>" \
        "		<li>git commit -m \"first commit\"</li>" \
        "		<li>git remote add origin https://github.com/mycompany/myproject.git</li>" \
        "		<li>git push origin gh-pages</li>" \
        "	<ul>" \
        "</p>" \
        "" \
        "<h3>" + QCoreApplication.translate("NoPublisher", "Clone a website") + "</h3>" \
        "<p>" + QCoreApplication.translate("NoPublisher", "If you already have published your website and want to download it from github use the following.") + "</p>" \
        "<p style=\"font-family: Courier;\">" \
        "    <ul>" \
        "	    <li>cd " + fsb_path + "</li>" \
        "		<li>cd sources</li>" \
        "		<li>git clone -b gh-pages https://github.com/mycompany/myproject.git MyProject</li>" \
        "	<ul>" \
        "</p>" \
        "</div>" \
        "</div>" \
        "</section>" \
        "</body>" \
        "</html>"
        self.browser.setHtml(html)