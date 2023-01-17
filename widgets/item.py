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

from PySide6.QtCore import Property, QObject


class Item(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._adminlabel = ""
        self._text = ""
        self._id = ""
        self.tag_name = ""
        self.display_name = ""

    @Property('QString')
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @Property('QString')
    def adminlabel(self):
        return self._adminlabel

    @adminlabel.setter
    def adminlabel(self, adminlabel):
        self._adminlabel = adminlabel

    def getAttributeQml(self, indent, att, value):
        qml = ""
        if value: 
            if isinstance(value, str):
                if att == "id":
                    qml += " " * indent + att + ":  " + value + "\n"
                else:
                    qml += " " * indent + att + ": \"" + value + "\"\n"
            elif isinstance(value, bool):
                qml += " " * indent + att + ": true\n"
            elif isinstance(value, int):
                qml += " " * indent + att + ": " + str(value) + "\n"
        return qml
