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

from PySide6.QtWidgets import  QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PySide6.QtCore import Qt, QUrl, Signal, QCoreApplication
from PySide6.QtGui import QPalette, QColor, QPixmap, QDrag, QUndoStack
from widgets.row import Row
from widgets.roweditor import RowEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.dropzone import DropZone
from widgets.widgetmimedata import WidgetMimeData
import resources

class SectionEditor(QWidget):
    sectionEditorCopied = Signal(object)

    def __init__(self, fullwidth):
        QWidget.__init__(self)
        from widgets.hyperlink import HyperLink
        from widgets.flatbutton import FlatButton
        from widgets.section import Section
        from widgets.content import ContentType
        from widgets.elementeditor import ElementEditor, Mode

        self.fullwidth = fullwidth
        self.section = None
        self.id = None
        self.cssclass = None
        self.style = None
        self.attributes = None
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        self.setBGColor()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(5)
        self.edit_button = FlatButton(":/images/edit_normal.png", ":/images/edit_hover.png")
        self.copy_button = FlatButton(":/images/copy_normal.png", ":/images/copy_hover.png")
        self.delete_button = FlatButton(":/images/trash_normal.png", ":/images/trash_hover.png")
        self.edit_button.setToolTip(QCoreApplication.translate("SectionEditor", "Edit Section"))
        self.delete_button.setToolTip(QCoreApplication.translate("SectionEditor", "Delete Section"))
        self.copy_button.setToolTip(QCoreApplication.translate("SectionEditor", "Copy Section"))
        self.edit_button.setMaximumWidth(24)
        self.copy_button.setMaximumWidth(24)
        self.delete_button.setMaximumWidth(24)
        vbox.addWidget(self.edit_button)
        vbox.addWidget(self.copy_button)
        vbox.addWidget(self.delete_button)

        vboxRight = QVBoxLayout()
        vboxRight.setAlignment(Qt.AlignLeft)
        layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        layout.addLayout(vbox)
        addRow = HyperLink(QCoreApplication.translate("SectionEditor", "(+) Add Row"))
        vboxRight.addLayout(self.layout)

        if self.fullwidth:
            ee = ElementEditor()
            ee.elementEnabled.connect(self.addElement)
            ee.elementDragged.connect(self.addElement)
            
            # connect(ee, SIGNAL(elementCopied(ElementEditor*)), self, SLOT(copyElement(ElementEditor*)))

            self.layout.addWidget(ee, 0, Qt.AlignTop)
        else:
            vboxRight.addWidget(addRow)
        layout.addLayout(vboxRight)
        self.setLayout(layout)

        self.delete_button.clicked.connect(self.delete)
        self.copy_button.clicked.connect(self.copy)
        addRow.clicked.connect(self.addRow)
        self.edit_button.clicked.connect(self.edit)

    def edit(self):
        ce = self.getContentEditor()
        if ce:
            ce.sectionEdit(self)

    def addRow(self):
        row = Row()
        self.section._items.append(row)
        re = RowEditor()
        re.load(row)
        self.addRowEditor(re)
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Add Row")

    def addRowEditor(self, re):
        re.rowEditorCopied.connect(self.copyRowEditor)
        self.layout.addWidget(re)

    def copyRowEditor(self, re):
        ren = RowEditor()
        row = re.row.clone()
        ren.load(row)
        self.section._items.append(row)
        self.addRowEditor(ren)
        ce = self.getContentEditor()
        if ce:
            ce.editChanged("Copy Row")

    def copy(self):
        self.sectionEditorCopied.emit(self)

    def delete(self):
        pe = self.parentWidget()
        if pe:
            pe.removeSection(self)

    def setBGColor(self):
        pal = self.palette()
        if self.fullwidth:
            pal.setColor(QPalette.Window, QColor("#800080"))
        else:
            pal.setColor(QPalette.Window, QColor(self.palette().base().color().name()))
        self.setPalette(pal)

    def addElement(self):
        ee = ElementEditor()
        self.layout.addWidget(ee, 0, Qt.AlignTop)
        ee.elementEnabled.connect(self.addElement)
        ee.elementDragged.connect(self.addElement)
        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), self, SLOT(copyElement(ElementEditor*)))

    def addElementEditor(self, ee):
        ee.elementEnabled.connect(self.addElement)
        ee.elementDragged.connect(self.addElement)

        # connect(ee, SIGNAL(elementCopied(ElementEditor*)), self, SLOT(copyElement(ElementEditor*)))
        self.layout.insertWidget(self.layout.count() - 1, ee, 0, Qt.AlignTop)

    def setSection(self, section):
        self.section = section

    def removeRowEditor(self, re):
        re.setVisible(False)
        self.layout.removeWidget(re)

    def load(self, section):
        from widgets.elementeditor import ElementEditor, Mode
        from widgets.roweditor import RowEditor

        self.section = section
        for i in range(self.section.itemCount()):
            item = self.section.item(i)
            if isinstance(item, Row):
                re = RowEditor()
                re.load(item)
                self.addRowEditor(re)
            else:
                ee = ElementEditor()
                ee.setContent(item)
                ee.setMode(Mode.ENABLED)
                self.addElementEditor(ee)

    def getContentEditor(self):
        pe = self.parentWidget()
        if pe:
            sa = pe.parentWidget()
            if sa:
                vp = sa.parentWidget()
                if vp:
                    cee = vp.parentWidget()
                    if cee:
                        return cee

        return None

    def dragEnterEvent(self, event):
        myData = event.mimeData()
        if myData:
            if not self.section.fullwidth and isinstance(myData.getData(), RowEditor):
                # insert a dropzone at the end
                self.layout.addWidget(DropZone(myData.width, myData.height))
                event.accept()
            elif self.section.fullwidth and isinstance(myData.getData(), ElementEditor):
                for i in range(self.layout.count()):
                    editor = self.layout.itemAt(i).widget()
                    if editor and editor.mode == Mode.EMPTY:
                        editor.setMode(Mode.DROPZONE)
                        break
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        # remove dropzones
        for i in range(self.layout.count()):
            dz = self.layout.itemAt(i).widget()
            if isinstance(dz, DropZone):
                dz.hide()
                self.layout.removeWidget(dz)
                del dz
                break
            
            editor = self.layout.itemAt(i).widget()
            if isinstance(editor, ElementEditor) and editor.mode == Mode.DROPZONE:
                # put editor to the end of the list
                editor.setMode(Mode.EMPTY)
                self.layout.removeWidget(editor)
                self.layout.addWidget(editor)
                break
        event.accept()
    

    def dragMoveEvent(self, event):
        myData = event.mimeData()
        if myData:
            re = myData.getData()
            if isinstance(re, RowEditor):
                height = 0
                row = 0

                # evaluate position for the dropzone to be placed
                for i in range(self.layout.count()):
                    editor = self.layout.itemAt(i).widget()
                    if isinstance(editor, RowEditor):
                        if event.pos().y() > height and event.pos().y() < height + editor.height():
                            break
                        height += editor.height()
                        row = row + 1

                # find dropzone and replace it to location
                for i in range(self.layout.count()):
                    dz = self.layout.itemAt(i).widget()
                    if isinstance(dz, DropZone):
                        if i != row:
                            self.layout.insertWidget(row, dz)
                        break
                
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                ee = myData.getData()
                if ee:
                    row = event.pos().y() / 50
                    for i in range(self.layout.count()):
                        editor = self.layout.itemAt(i).widget()
                        if editor and editor.mode == Mode.DROPZONE:
                            if i != row:
                                # put dropzone under mouse pointer
                                self.layout.insertWidget(row, editor)
                            break
                    event.setDropAction(Qt.MoveAction)
                    event.accept()
                else:
                    event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        myData = event.mimeData()
        if myData:
            re = myData.getData()
            if isinstance(re, RowEditor):
                # place the dragged RowEditor to the place where DropZone is now
                for i in range(self.layout.count()):
                    dz = self.layout.itemAt(i).widget()
                    if isinstance(dz, DropZone):
                        dz.hide()
                        self.layout.replaceWidget(dz, re)
                        new_pos = i
                        re.show()
                        del dz
                        break
                
                ce = self.getContentEditor()
                if ce:
                    myData.source_list.remove(re.row)
                    self.section.insertElement(re.row, new_pos)
                    ce.editChanged("Move Row")
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                ee = myData.getData()
                if isinstance(ee, ElementEditor):
                    for i in range(self.layout.count()):
                        dz = self.layout.itemAt(i).widget()
                        if isinstance(dz, ElementEditor) and dz.mode == Mode.DROPZONE:
                            # remove widget if it belongs to self layout
                            self.layout.removeWidget(ee)

                            # replace dropzone with dragged element
                            self.layout.replaceWidget(dz, ee)
                            new_pos = i
                            # and put dropzone to the end of the list
                            dz.setMode(Mode.EMPTY)
                            self.layout.removeWidget(dz)
                            self.layout.addWidget(dz)
                            break
                    ee.dropped()
                    ee.show()
                    ee.elementEnabled.disconnect()
                    ee.elementDragged.disconnect()
                    # ee.elementCopied.disconnect()
                    ee.elementEnabled.connect(self.addElement)
                    ee.elementDragged.connect(self.addElement)
                    # ee.elementCopied.connect(self.copyElement)

                    ce = self.getContentEditor()
                    if ce:
                        myData.source_list.remove(ee.content)
                        self.section.insertElement(ee.content, new_pos)
                        ce.editChanged("Move Element")
                    event.setDropAction(Qt.MoveAction)
                    event.accept()
                else:
                    event.ignore()
        else:
            event.ignore()
    
    def enableColumnAcceptDrop(self, mode):
        for i in range(self.layout.count()):
            re = self.layout.itemAt(i).widget()
            if isinstance(re, RowEditor):
                re.enableColumnAcceptDrop(mode)

    def mousePressEvent(self,event):
        mimeData = WidgetMimeData()
        mimeData.setSize(self.size().width(), self.size().height())
        mimeData.setData(self)

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())
        drag.setPixmap(pixmap)

        pe = self.parentWidget()
        pe.removeSectionEditor(self)
        pe.enableColumnAcceptDrop(False)
        pe.enableSectionAcceptDrop(False)
        self.hide()

        if drag.exec(Qt.MoveAction) == Qt.IgnoreAction:
            pe.addSection(self)
            self.show()
        
        pe.enableColumnAcceptDrop(True)
        pe.enableSectionAcceptDrop(True)

    def removeElement(self, content):
        self.section._items.remove(content)