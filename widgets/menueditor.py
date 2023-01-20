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
from widgets.animateableeditor import AnimateableEditor
from widgets.flatbutton import FlatButton
from widgets.menuitem import Menuitem
from widgets.imageselector import ImageSelector
from PySide6.QtWidgets import QFileDialog, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QTreeWidgetItem, QPushButton, QTreeWidget, QHeaderView, QAbstractItemView
from PySide6.QtCore import Signal, Qt, QFileInfo, QFile, QCoreApplication
from PySide6.QtGui import QImage
import resources

class MenuEditorTableCellButtons(QWidget):
    deleteItem = Signal(object)
    editItem = Signal(object)
    itemLeft = Signal(object)
    itemRight = Signal(object)
    itemUp = Signal(object)
    itemDown = Signal(object)

    def __init__(self):
        QWidget.__init__(self)
        self.delete = FlatButton(":/images/trash_normal.png", ":/images/trash_hover.png")
        self.edit = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
        self.left = FlatButton(":/images/left_normal.png", ":/images/left_hover.png", "", ":/images/left_disabled.png")
        self.right = FlatButton(":/images/right_normal.png", ":/images/right_hover.png", "", ":/images/right_disabled.png")
        self.up = FlatButton(":/images/up_normal.png", ":/images/up_hover.png", "", ":/images/up_disabled.png")
        self.down = FlatButton(":/images/down_normal.png", ":/images/down_hover.png", "", ":/images/down_disabled.png")
        self.edit.setToolTip(QCoreApplication.translate("MenuEditor", "Edit Item"))
        self.delete.setToolTip(QCoreApplication.translate("MenuEditor", "Delete Item"))
        self.left.setToolTip(QCoreApplication.translate("MenuEditor", "Make Mainitem"))
        self.right.setToolTip(QCoreApplication.translate("MenuEditor", "Make Subitem"))
        self.up.setToolTip(QCoreApplication.translate("MenuEditor", "Sort Up"))
        self.down.setToolTip(QCoreApplication.translate("MenuEditor", "Sort Down"))
        self.left.setEnabled(False)
        self.right.setEnabled(False)
        self.up.setEnabled(False)
        self.down.setEnabled(False)
        self.item = None

        hbox = QHBoxLayout()
        hbox.addWidget(self.edit)
        hbox.addWidget(self.up)
        hbox.addWidget(self.down)
        hbox.addWidget(self.left)
        hbox.addWidget(self.right)
        hbox.addWidget(self.delete)
        self.setLayout(hbox)

        self.delete.clicked.connect(self.deleteItemClicked)
        self.edit.clicked.connect(self.editItemClicked)
        self.left.clicked.connect(self.itemLeftClicked)
        self.right.clicked.connect(self.itemRightClicked)
        self.up.clicked.connect(self.itemUpClicked)
        self.down.clicked.connect(self.itemDownClicked)

    def setMenuItem(self, m):
        self.item = m

    def deleteItemClicked(self):
        self.deleteItem.emit(self.item)

    def editItemClicked(self):
        self.editItem.emit(self.item)

    def itemLeftClicked(self):
        self.itemLeft.emit(self.item)

    def itemRightClicked(self):
        self.itemRight.emit(self.item)

    def itemUpClicked(self):
        self.itemUp.emit(self.item)

    def itemDownClicked(self):
        self.itemDown.emit(self.item)

    def setEnableLeft(self, mode):
        self.left.setEnabled(mode)

    def setEnableRight(self, mode):
        self.right.setEnabled(mode)

    def setEnableUp(self, mode):
        self.up.setEnabled(mode)

    def setEnableDown(self, mode):
        self.down.setEnabled(mode)


class MenuEditor(AnimateableEditor):
    contentChanged = Signal(object)
    menuChanged = Signal(str)

    def __init__(self, win, menu, site):
        AnimateableEditor.__init__(self)
        self.win = win
        self.menu = menu
        self.site = site
        self.changed = False

        self.setAutoFillBackground(True)

        titleLabel = QLabel(QCoreApplication.translate("MenuEditor", "Menu Editor"))
        fnt = titleLabel.font()
        fnt.setPointSize(20)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        self.close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        self.close.setToolTip("Close Content Editor")
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
        hbox.addWidget(self.close)

        addButton = QPushButton(QCoreApplication.translate("MenuEditor", "Add Menuitem"))
        addButton.setMaximumWidth(200)

        self.name = QLineEdit()
        self.name.setText(menu.name)
        self.name.setMaximumWidth(200)

        labels = [QCoreApplication.translate("MenuEditor", "Title"), QCoreApplication.translate("MenuEditor", "Url"), QCoreApplication.translate("MenuEditor", "Icon"), "", QCoreApplication.translate("MenuEditor", "Sort")]

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(labels)
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tree.header().hideSection(4)
        self.tree.setSelectionMode(QAbstractItemView.NoSelection)
        self.tree.setToolTip(QCoreApplication.translate("MenuEditor", "Double Click To Edit"))
        self.tree.setColumnWidth(2, 40)

        layout = QGridLayout()
        layout.addWidget(titleLabel, 0, 0)
        layout.addLayout(hbox, 0, 2)
        layout.addWidget(QLabel(QCoreApplication.translate("MenuEditor", "Name")), 1, 0)
        layout.addWidget(self.name, 2, 0)
        layout.addWidget(addButton, 3, 0)
        layout.addWidget(self.tree, 4, 0, 1, 3)
        self.setLayout(layout)

        self.reloadMenu(menu)

        addButton.clicked.connect(self.addButtonClicked)
        self.close.clicked.connect(self.closeEditor)
        self.name.editingFinished.connect(self.nameChanged)
        self.redo.clicked.connect(self.redoEdit)
        self.undo.clicked.connect(self.undoEdit)
        self.tree.itemChanged.connect(self.itemChanged)

    def reloadMenu(self, menu):
        if not menu:
            self.close.emit()
            return

        self.menu = menu
        self.tree.clear()

        self.name.setText(menu.name)
        for i in range(self.menu.itemCount()):
            item = self.menu.item(i)
            self.addTreeItem(item)

        self.tree.expandAll()
        self.tree.sortItems(4, Qt.AscendingOrder)
        self.updateButtonStates()

    def addTreeItem(self, item):
        twi = QTreeWidgetItem()
        twi.setFlags(twi.flags() | Qt.ItemIsEditable)
        twi.setText(0, item.title)
        twi.setText(1, item.url)

        twi.setText(4, str(self.tree.topLevelItemCount()))
        twi.setData(0, Qt.UserRole, item)
        self.tree.addTopLevelItem(twi)
        self.addTableCellButtons(item, twi)

        for i in range(item.itemCount()):
            sub = item.item(i)
            stwi = QTreeWidgetItem()
            stwi.setFlags(stwi.flags() | Qt.ItemIsEditable)
            stwi.setText(0, sub.title)
            stwi.setText(1, sub.url)
            stwi.setText(4, str(i))
            stwi.setData(0, Qt.UserRole, sub)
            twi.addChild(stwi)
            self.addTableCellButtons(sub, stwi)

    def addTableCellButtons(self, item, twi):
        tcb = MenuEditorTableCellButtons()
        tcb.setMenuItem(item)
        self.tree.setItemWidget(twi, 3, tcb)
        self.tree.setColumnWidth(3, tcb.sizeHint().width())
        if item.isSubitem():
            tcb.deleteItem.connect(self.deleteSubItem)
            tcb.itemLeft.connect(self.itemLeft)
            tcb.editItem.connect(self.editSubItem)
        else:
            tcb.deleteItem.connect(self.deleteItem)
            tcb.itemUp.connect(self.itemUp)
            tcb.itemDown.connect(self.itemDown)
            tcb.itemRight.connect(self.itemRight)
            tcb.editItem.connect(self.editItem)

        imgs = ImageSelector()
        imgs.setToolTip(QCoreApplication.translate("MenuEditor", "Click to select image, right click to reset image"))
        imgs.setItem(item)
        imgs.setMaximumSize(24, 24)
        isw = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(imgs)
        isw.setLayout(vbox)
        if not item.icon:
            imgs.setImage(QImage(":/images/image_placeholder.png"))
        else:
            imgs.setImage(QImage(self.site.source_path + "/" + item.icon))
        self.tree.setItemWidget(twi, 2, isw)
        imgs.clicked.connect(self.iconClicked)

    def registerUndoStack(self, stack):
        self.undoStack = stack
        self.undoStack.canUndoChanged.connect(self.canUndoChanged)
        self.undoStack.canRedoChanged.connect(self.canRedoChanged)
        self.undoStack.undoTextChanged.connect(self.undoTextChanged)
        self.undoStack.redoTextChanged.connect(self.redoTextChanged)
        self.undo.setEnabled(self.undoStack.canUndo())
        self.redo.setEnabled(self.undoStack.canRedo())
        self.undo.setToolTip(QCoreApplication.translate("general", "Undo") + " " + self.undoStack.undoText())
        self.redo.setToolTip(QCoreApplication.translate("general", "Redo") + " " + self.undoStack.redoText())

    def canUndoChanged(self, can):
        self.undo.setEnabled(can)

    def canRedoChanged(self, can):
        self.redo.setEnabled(can)

    def undoTextChanged(self, text):
        self.undo.setToolTip(QCoreApplication.translate("general", "Undo") + " " + text)

    def redoTextChanged(self, text):
        self.redo.setToolTip(QCoreApplication.translate("general", "Redo") + " " + text)

    def getUndoRedoText(self, item, action):
        return "menuitem (" + item.title + ") from menu (" + self.menu.name + ") " + action

    def undoEdit(self):
        self.undoStack.undo()

    def redoEdit(self):
        self.undoStack.redo()

    def addButtonClicked(self):
        menuitem = Menuitem()
        self.menu.addMenuitem(menuitem)
        self.addTreeItem(menuitem)
        self.menuChanged.emit(self.getUndoRedoText(menuitem, "added"))

        self.updateButtonStates()
        item = self.tree.topLevelItem(self.getRow(menuitem))
        self.tree.editItem(item, 0)

    def closeEditor(self):
        self.closes.emit()

    def nameChanged(self):
        if self.menu.name != self.name.text:
            action = "menu name changed from \"" + self.menu.name + "\" to \"" + self.name.text + "\""
            self.menu.setName(self.name.text())
            self.contentChanged.emit(self.menu)
            self.menuChanged.emit(action)

    def itemChanged(self, twi, column):
        action = ""
        item = twi.data(0, Qt.UserRole)
        if column == 0:
            item.title = twi.text(0)
            action = "title changed"
        elif column == 1:
            item.url = twi.text(1)
            action = "url changed"
        self.menuChanged.emit(self.getUndoRedoText(item, action))

    def getRow(self, menuitem):
        for i in range(0, self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            mi = item.data(0, Qt.UserRole)
            if mi == menuitem:
                return i
        return -1

    def deleteItem(self, menuitem):
        print("delete item", menuitem)

    def deleteSubItem(self, menuitem):
        row = self.getRow(menuitem.parentItem)
        parent = self.tree.topLevelItem(row)
        if parent:
            for i in range(0, parent.childCount()):
                child = parent.child(i)
                mi = child.data(0, Qt.UserRole)
                if mi == menuitem:
                    parent.removeChild(child)
                    del child
                    break

        if menuitem.parentItem:
            menuitem.parentItem.removeMenuitem(menuitem)

        self.updateButtonStates()
        self.menuChanged.emit(self.getUndoRedoText(menuitem, "deleted"))

    def itemUp(self, menuitem):
        row = self.getRow(menuitem)
        sortItem1 = self.tree.topLevelItem(row - 1)
        sortItem2 = self.tree.topLevelItem(row)
        sortItem1.setText(4, str(row))
        sortItem2.setText(4, str(row - 1))
        self.tree.sortItems(4, Qt.AscendingOrder)
        self.resort()
        self.updateButtonStates()
        self.menuChanged.emit(self.getUndoRedoText(menuitem, "sorted up"))


    def itemDown(self, menuitem):
        row = self.getRow(menuitem)
        sortItem1 = self.tree.topLevelItem(row)
        sortItem2 = self.tree.topLevelItem(row + 1)
        sortItem1.setText(4, str(row + 1))
        sortItem2.setText(4, str(row))
        self.tree.sortItems(4, Qt.AscendingOrder)
        self.resort()
        self.updateButtonStates()
        self.menuChanged.emit(self.getUndoRedoText(menuitem, "sorted down"))

    def editItem(self, menuitem):
        item = self.tree.topLevelItem(self.getRow(menuitem))
        self.tree.editItem(item, 0)

    def editSubItem(self, menuitem):
        row = self.getRow(menuitem.parentItem)
        parent = self.tree.topLevelItem(row)
        for i in range(parent.childCount()):
            child = parent.child(i)
            mi = child.data(0, Qt.UserRole)
            if mi == menuitem:
                self.tree.editItem(child, 0)
                break

    def itemLeft(self, menuitem):
        row = self.getRow(menuitem.parentItem)
        parent = self.tree.topLevelItem(row)
        for i in range(parent.childCount()):
            child = parent.child(i)
            mi = child.data(0, Qt.UserRole)
            if mi == menuitem:
                menuitem.parentItem.removeMenuitem(menuitem)
                self.menu.addMenuitem(menuitem)
                parent.takeChild(i)
                self.addTreeItem(menuitem)
                break

        self.updateButtonStates()
        self.menuChanged.emit(self.getUndoRedoText(menuitem, "changed to top item"))

    def itemRight(self, menuitem):
        row = self.getRow(menuitem)
        parent = self.tree.topLevelItem(row - 1)
        item = self.tree.takeTopLevelItem(row)
        parent.addChild(item)
        self.menu.removeItem(menuitem)
        parentItem = parent.data(0, Qt.UserRole)
        parentItem.addMenuitem(menuitem)
        self.addTableCellButtons(menuitem, item)
        self.tree.expandAll()
        self.updateButtonStates()
        self.menuChanged.emit(self.getUndoRedoText(menuitem, "changed to sub item"))



    def iconClicked(self, itemselector, button):
        mi = itemselector.item()
        action = ""
        if button == Qt.LeftButton:
            fileName = ""
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setNameFilter(QCoreApplication.translate("MenuEditor", "Images") + " (*.png *.gif *.jpg)All (*)")
            dialog.setWindowTitle(QCoreApplication.translate("MenuEditor", "Load Image"))
            dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            if dialog.exec_():
                fileName = dialog.selectedFiles().first()
            del dialog
            if not fileName:
                return

            # copy file to assets dir
            info = QFileInfo(fileName)
            name = info.fileName().replace(" ", "_")
            path = os.path.join(self.site.source_path, "assets", "images", name)
            QFile.copy(fileName, path)

            # also copy file to deploy dir for previews
            dpath = os.path.join(self.site.source_path, self.site.output, "assets", "images", name)
            QFile.copy(fileName, dpath)

            mi.setIcon(path.mid(path.indexOf("assets/images/")))
            itemselector.setImage(QImage(path))
            action = "icon changed"

        elif button == Qt.RightButton:
            action = "icon removed"
            mi.setIcon("")
            itemselector.setImage(QImage(":/images/image_placeholder.png"))

        self.menuChanged.emit(self.getUndoRedoText(mi, action))

    def updateButtonStates(self):
        for i in range(0, self.tree.topLevelItemCount()):
            twi = self.tree.topLevelItem(i)
            tcb = self.tree.itemWidget(twi, 3)
            menuitem = twi.data(0, Qt.UserRole)
            tcb.setEnableDown(i != self.tree.topLevelItemCount() - 1)
            tcb.setEnableUp(i != 0)
            tcb.setEnableRight(i != 0 and menuitem.itemCount() == 0)
            tcb.setEnableLeft(False)
            for j in range(0, twi.childCount()):
                stwi = twi.child(j)
                stcb = self.tree.itemWidget(stwi, 3)
                stcb.setEnableLeft(True)

    def resort(self):
        while self.menu.itemCount() > 0:
            self.menu.removeItem(self.menu.item(0))

        for i in range(0, self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            mi = item.data(0, Qt.UserRole)
            self.menu.addMenuitem(mi)

