
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

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Slot, Signal


class HyperLink(QLabel):
    clicked = Signal()

    def __init__(self, text):
        QLabel.__init__(self)
        self.autohover = True
        self.text = text
        self.color = self.palette().link().color().name()
        self.hover = self.palette().highlight().color().name()
        super().setText("<a style=\"color: " + self.color + "; text-decoration: none; cursor: pointer;\" href=\"#/\">" + self.text + "</a>")
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setCursor(Qt.PointingHandCursor)
        self.linkActivated.connect(self.linkActivated2)

    @Slot(str)
    def linkActivated2(self, link):
        self.clicked.emit()

    def setText(self, text):
        self.text = text
        super().setText("<a style=\"color: " + self.color + "; text-decoration: none; cursor: pointer;\" href=\"#/\">" + self.text + "</a>")

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        event.accept()
        self.clicked.emit()

    def enterEvent(self, event):
        if self.autohover:
            super().setText("<a style=\"color: " + self.hover + "; text-decoration: none; cursor: pointer;\" href=\"#/\">" + self.text + "</a>")

    def leaveEvent(self, event):
        if self.autohover:
            super().setText("<a style=\"color: " + self.color + "; text-decoration: none; cursor: pointer;\" href=\"#/\">" + self.text + "</a>")

    def setColor(self, color):
        self.color = color
        super().setText("<a style=\"color: " + self.color + " text-decoration: none cursor: pointer\" href=\"#/\">" + self.text + "</a>")

    def setHovered(self, hovered):
        if hovered:
            super().setText("<a style=\"color: " + self.hover + " text-decoration: none cursor: pointer\" href=\"#/\">" + self.text + "</a>")
        else:
            super().setText("<a style=\"color: " + self.color + " text-decoration: none cursor: pointer\" href=\"#/\">" + self.text + "</a>")

    def setAutohover(self, value):
        super().autohover = value
