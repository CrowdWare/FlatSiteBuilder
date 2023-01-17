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

from widgets.undoableeditor import UndoableEditor
from widgets.tablecellbuttons import TableCellButtons
from widgets.menu import Menu
from PySide6.QtWidgets import QPushButton, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from PySide6.QtCore import Signal, Qt, QCoreApplication


class MenuList(UndoableEditor):
    editContent = Signal(object)
    editedItemChanged = Signal(object)

    def __init__(self, win, site):
        UndoableEditor.__init__(self)
        self.win = win
        self.site = site
        self.menuInEditor = None
        self.editor = None
        self.titleLabel.setText(QCoreApplication.translate("MenuList", "Menus"))
        self.filename = site.source_path + "/Menus.qml"
        button = QPushButton(QCoreApplication.translate("MenuList", "Add Menu"))
        button.setMaximumWidth(200)

        self.list = QTableWidget(0, 2, self)
        self.list.verticalHeader().hide()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.list.setToolTip(QCoreApplication.translate("MenuList", "Double click to edit item"))
        labels = ["", QCoreApplication.translate("MenuList", "Name")]
        self.list.setHorizontalHeaderLabels(labels)

        self.layout.addWidget(button, 1, 0)
        self.layout.addWidget(self.list, 2, 0, 1, 3)

        self.load()

        button.clicked.connect(self.buttonClicked)
        self.list.cellDoubleClicked.connect(self.tableDoubleClicked)

    def load(self):
        self.list.clearContents()
        self.list.setRowCount(0)
        self.site.loadMenus()

        menuId = -1
        if self.menuInEditor:
            menuId = self.menuInEditor.id()
        self.menuInEditor = None
        if(self.site.menus == None):
            return
        for i in range(self.site.menus.menuCount()):
            menu = self.site.menus.menu(i)
            item = self.addListItem(menu)
            if menu.id == menuId:
                self.list.selectRow(self.list.rowCount() - 1)
                self.menuInEditor = menu
                self.editedItemChanged.emit(item)
        if self.editor:
            self.editor.reloadMenu(self.menuInEditor)

    def addListItem(self, menu):
        rows = self.list.rowCount()
        self.list.setRowCount(rows + 1)
        tcb = TableCellButtons()
        tcb.setItem(menu)
        tcb.deleteItem.connect(self.deleteMenu)
        tcb.editItem.connect(self.editMenu)
        self.list.setCellWidget(rows, 0, tcb)
        self.list.setRowHeight(rows, tcb.sizeHint().height())
        titleItem = QTableWidgetItem(menu.name)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        titleItem.setData(Qt.UserRole, menu)
        self.list.setItem(rows, 1, titleItem)
        return titleItem

    def registerMenuEditor(self, editor):
        self.editor = editor
        self.editor.registerUndoStack(self.undoStack)
        self.editor.menuChanged.connect(self.menuChanged)

    def unregisterMenuEditor(self):
        self.editor = None

    def deleteMenu(self, menu):
        for row in range(0, self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == menu:
                self.site.removeMenu(m)
                self.list.removeRow(row)
                self.menuChanged("menu \"" + m.name + "\" deleted")
                break

    def editMenu(self, menu):
        for row in range(0, self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == menu:
                self.menuInEditor = m
                self.list.selectRow(row)
                self.editContent.emit(item)
                break

    def save(self):
        self.site.saveMenus()

    def menuChanged(self, text):
        self.contentChanged(text)

    def tableDoubleClicked(self, r, b):
        item = self.list.item(r, 1)
        self.menuInEditor = item.data(Qt.UserRole)
        self.editContent.emit(item)

    def buttonClicked(self):
        menu = Menu()
        self.site.addMenu(menu)
        self.addListItem(menu)
        self.list.selectRow(self.list.rowCount() - 1)
        self.menuChanged("menu added")
        self.tableDoubleClicked(self.list.rowCount() - 1, 0)
