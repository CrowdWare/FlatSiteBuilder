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
from widgets.content import ContentType
from widgets.flatbutton import FlatButton
from widgets.tablecellbuttons import TableCellButtons
#from widgets.commands import DeleteContentCommand
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QTableWidget, QAbstractItemView, QHeaderView
from PySide6.QtCore import Signal, Qt, QFileInfo, QCoreApplication
from PySide6.QtGui import QUndoStack
import resources

class ContentList(QWidget):
    editContent = Signal(object)

    def __init__(self, site, type):
        QWidget.__init__(self)
        self.site = site
        self.addedContentName = ""
        self.type = type
        self.undoStack = QUndoStack()
        vbox = QVBoxLayout()
        layout = QGridLayout()
        titleLabel = QLabel()
        button = QPushButton()
        if self.type == ContentType.PAGE:
            button.setText(QCoreApplication.translate("ContentList", "Add Page"))
        else:
            button.setText(QCoreApplication.translate("ContentList", "Add Post"))
        button.setMaximumWidth(120)
        if self.type == ContentType.PAGE:
            titleLabel.setText(QCoreApplication.translate("ContentList", "Pages"))
        else:
            titleLabel.setText(QCoreApplication.translate("ContentList", "Posts"))
        fnt = titleLabel.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        self.undo = FlatButton(":/images/undo_normal.png", ":/images/undo_hover.png", "", ":/images/undo_disabled.png")
        self.redo = FlatButton(":/images/redo_normal.png", ":/images/redo_hover.png", "", ":/images/redo_disabled.png")
        self.undo.setToolTip(QCoreApplication.translate("general", "Undo"))
        self.redo.setToolTip(QCoreApplication.translate("general", "Redo"))
        self.undo.setEnabled(False)
        self.redo.setEnabled(False)
        hbox = QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(self.undo)
        hbox.addWidget(self.redo)

        self.list = QTableWidget(0, 6, self)
        self.list.verticalHeader().hide()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.list.setToolTip(QCoreApplication.translate("ContentList", "Double click to edit item"))
        labels = ["", QCoreApplication.translate("ContentList", "Name"), QCoreApplication.translate("ContentList", "Source"), QCoreApplication.translate("ContentList", "Layout"), QCoreApplication.translate("ContentList", "Author"), QCoreApplication.translate("ContentList", "Date")]
        self.list.setHorizontalHeaderLabels(labels)
        self.list.setSortingEnabled(True)

        self.reload()

        layout.addWidget(titleLabel, 0, 0)
        layout.addLayout(hbox, 0, 2)
        layout.addWidget(button, 1, 0)
        layout.addWidget(self.list, 2, 0, 1, 3)
        vbox.addLayout(layout)
        self.setLayout(vbox)

        button.clicked.connect(self.addPage)
        self.list.cellDoubleClicked.connect(self.tableDoubleClicked)
        self.redo.clicked.connect(self.doredo)
        self.undo.clicked.connect(self.doundo)
        self.undoStack.canUndoChanged.connect(self.canUndoChanged)
        self.undoStack.canRedoChanged.connect(self.canRedoChanged)
        self.undoStack.redoTextChanged.connect(self.redoTextChanged)

    def reload(self):
        self.list.setRowCount(0)
        row = -1

        itemToEdit = None
        if self.type == ContentType.PAGE:
            self.site.loadPages()
            for i in range(len(self.site.pages)):
                content = self.site.pages[i]
                self.addListItem(content)
                if content.source == self.addedContentName:
                    row = self.list.rowCount() - 1
                    itemToEdit = self.list.item(row, 1)
        else:
            self.site.loadPosts()
            # todo, do sort here
            self.site.posts.sort(key=self.sortPost, reverse=True)
            for i in range(0, len(self.site.posts)):
                content = self.site.posts[i]
                self.addListItem(content)
                if content.source == self.addedContentName:
                    row = self.list.rowCount() - 1

        if itemToEdit:
            self.addedContentName = ""
            self.list.selectRow(row)
            self.editContent.emit(itemToEdit)

    def sortPost(self, a):
        return a.date

    def addListItem(self, content):
        rows = self.list.rowCount()
        self.list.setRowCount(rows + 1)
        tcb = TableCellButtons()
        tcb.setItem(content)
        #tcb.deleteItem.connect(self.deleteContent)
        tcb.editItem.connect(self.edit)
        self.list.setCellWidget(rows, 0, tcb)
        self.list.setRowHeight(rows, tcb.sizeHint().height())

        titleItem = QTableWidgetItem(content.title)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        titleItem.setData(Qt.UserRole, content)
        self.list.setItem(rows, 1, titleItem)

        sourceItem = QTableWidgetItem(content.source)
        sourceItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 2, sourceItem)

        layoutItem = QTableWidgetItem(content.layout)
        layoutItem.setFlags(layoutItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 3, layoutItem)

        authorItem = QTableWidgetItem(content.author)
        authorItem.setFlags(authorItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 4, authorItem)
        dateItem = QTableWidgetItem(content.date.toString("dd.MM.yyyy"))
        dateItem.setFlags(dateItem.flags() ^ Qt.ItemIsEditable)
        self.list.setItem(rows, 5, dateItem)

    def canUndoChanged(self, can):
        self.undo.setEnabled(can)

    def canRedoChanged(self, can):
        self.redo.setEnabled(can)

    def undoTextChanged(self, text):
        self.undo.setToolTip("Undo " + text)

    def redoTextChanged(self, text):
        self.redo.setToolTip("Redo " + text)

    def doundo(self):
        self.undoStack.undo()

    def doredo(self):
        self.undoStack.redo()

    def addPage(self):
        self.addedContentName = self.site.createTemporaryContent(self.type)
        info = QFileInfo(self.addedContentName)
        self.addedContentName = info.fileName()
        self.reload()

    def tableDoubleClicked(self, r, i):
        item = self.list.item(r, 1)
        self.undoStack.clear()
        self.editContent.emit(item)

    def edit(self, content):
        for row in range(self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == content:
                self.list.selectRow(row)
                self.undoStack.clear()
                self.editContent.emit(item)
                break

"""     def deleteContent(self, content):
        for row in range(self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == content:
                if m.content_type == ContentType.PAGE:
                    subdir = "pages"
                else:
                    subdir = "posts"
                delCommand = DeleteContentCommand(self, os.path.join(self.site.source_path, subdir, m.source), "delete content " + m.title)
                self.undoStack.push(delCommand)
                break 
"""
