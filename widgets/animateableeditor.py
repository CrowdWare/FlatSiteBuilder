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

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Property


class AnimateableEditor(QWidget):
    closes = Signal()

    def __init__(self):
        QWidget.__init__(self)
        self._changed = False

    def contentChanged(self):
        self._changed = True

    @Property('bool')
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, value):
        self._changed = value

    @Property('int')
    def x(self):
        return super().x()

    @x.setter
    def x(self, value):
        self.move(value, super().y())

    @Property('int')
    def y(self):
        return super().y()

    @y.setter
    def y(self, value):
        self.move(super().x(), value)

    @Property('int')
    def width(self):
        return super().width()

    @width.setter
    def width(self, value):
        self.resize(value, super().height())

    @Property('int')
    def height(self):
        return super().height()

    @height.setter
    def height(self, value):
        self.resize(super().width(), value)
