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

from widgets.menu import Menu
from PySide6.QtCore import QObject, ClassInfo
from PySide6.QtQml import ListProperty


@ClassInfo(DefaultProperty = 'menus')
class Menus(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)

        self._menus = []


    def menu(self, n):
        return self._menus[n]

    def menuCount(self):
        return len(self._menus)

    def appendMenu(self, menu):
        self._menus.append(menu)

    menus = ListProperty(Menu, appendMenu)
