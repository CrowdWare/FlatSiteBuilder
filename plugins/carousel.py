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
#  along with FlatSiteBuilder.  If not, see <http.//www.gnu.org/licenses/>.
#
#############################################################################

import html
from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from widgets.flatbutton import FlatButton
from widgets.tablecellbuttons import TableCellButtons
from widgets.animateableeditor import AnimateableEditor
from widgets.imageselector import ImageSelector
from plugins.texteditor import XmlHighlighter 
from PySide6.QtQml import qmlRegisterType, ListProperty
from PySide6.QtCore import ClassInfo, Qt, Signal, Property, QObject, QDir, QFile, QPoint, QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation, QCoreApplication
from PySide6.QtGui import QImage, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QTextEdit, QTableWidgetItem, QLineEdit, QGridLayout, QLabel, QPushButton, QTableWidget, QAbstractItemView, QHeaderView
import plugins.carousel_rc


class CarouselEditor(ElementEditorInterface):
    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.class_name = "CarouselEditor"
        self.display_name = QCoreApplication.translate("CarouselEditor", "Carousel")
        self.tag_name = "Carousel"
        self.version = "1.0"
        self.icon = QImage(":/carousel.png")

        self.changed = False
        #self.editor = 0
        self.setAutoFillBackground(True)

        grid = QGridLayout()
        self.id = QLineEdit()
        self.id.setMaximumWidth(200)
        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)
        titleLabel = QLabel(QCoreApplication.translate("CarouselEditor", "Carousel Module"))
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip(QCoreApplication.translate("general", "Close Editor"))

        addSlide = QPushButton(QCoreApplication.translate("CarouselEditor", "Add Slide"))
        addSlide.setMaximumWidth(120)

        self.list = QTableWidget(0, 2, self)
        self.list.verticalHeader().hide()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch )
        self.list.setToolTip(QCoreApplication.translate("CarouselEditor", "Double click to edit item"))
        labels = ["", "Name"]
        self.list.setHorizontalHeaderLabels(labels)

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 2, 1, 1, Qt.AlignRight)
        grid.addWidget(addSlide, 1, 0)
        grid.addWidget(self.list, 2, 0, 1, 3)
        grid.addWidget(QLabel("Id"), 4, 0)
        grid.addWidget(self.id, 5, 0)
        grid.addWidget(QLabel(QCoreApplication.translate("CarouselEditor", "Admin Label")), 6, 0)
        grid.addWidget(self.adminlabel, 7, 0)

        self.setLayout(grid)

        addSlide.clicked.connect(self.addSlide)
        self.adminlabel.textChanged.connect(self.contentChanged)
        self.id.textChanged.connect(self.contentChanged)
        close.clicked.connect(self.closeEditor)
        self.list.cellDoubleClicked.connect(self.tableDoubleClicked)

        self.installEventFilter(self)

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.id = self.id.text()
                self.content.adminlabel = self.adminlabel.text()
        self.close.emit()

    def setContent(self, content):
        self.content = content
        if content:
            self.id.setText(content.id)
            self.adminlabel.setText(content.adminlabel)
            self.changed = False

    def getContent(self):
        return self.content

    def registerContenType(self):
        qmlRegisterType(Carousel, 'Carousel', 1, 0, 'Carousel')
        qmlRegisterType(Slide, 'Carousel', 1, 0, 'Slide')

    def getImportString(self):
        return "import Carousel 1.0\n"

    def getDefaultContent(self):
        return Carousel()

    def addSlide(self):
        slide = Slide()
        self.addListItem(slide)
        self.contentChanged()
        self.tableDoubleClicked(self.list.rowCount() - 1)

    def addListItem(self, slide):
        rows = self.list.rowCount()
        self.list.setRowCount(rows + 1)
        tcb = TableCellButtons()
        tcb.setItem(slide)
        tcb.deleteItem.connect(self.deleteSlide)
        tcb.editItem.connect(self.editSlide)
        self.list.setCellWidget(rows, 0, tcb)
        self.list.setRowHeight(rows, tcb.sizeHint().height())
        titleItem = QTableWidgetItem(slide.title)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)
        titleItem.setData(Qt.UserRole, slide)
        self.list.setItem(rows, 1, titleItem)

    def tableDoubleClicked(self, row):
        item = self.list.item(row, 1)
        slide = item.data(Qt.UserRole)

        self.editor = SlideEditor()
        #self.editor.setSite(self.site)
        self.editor.setSlide(slide)
        self.editor.closes.connect(self.editorClosed)
        self.animate(item)

    def animate(self, item):
        self.row = item.row()

        # create a cell widget to get the right position in the table
        self.sourcewidget = QWidget()
        self.list.setCellWidget(self.row, 1, self.sourcewidget)
        pos = self.sourcewidget.mapTo(self, QPoint(0,0))

        self.editor.setParent(self)
        self.editor.move(pos)
        self.editor.resize(self.sourcewidget.size())
        self.editor.show()

        self.animationgroup = QParallelAnimationGroup()
        self.animx = QPropertyAnimation()
        self.animx.setDuration(300)
        self.animx.setStartValue(pos.x())
        self.animx.setEndValue(0)
        self.animx.setTargetObject(self.editor)
        self.animx.setPropertyName("x".encode("utf-8"))
        self.animationgroup.addAnimation(self.animx)
        self.animy = QPropertyAnimation()
        self.animy.setDuration(300)
        self.animy.setStartValue(pos.y())
        self.animy.setEndValue(0)
        self.animy.setTargetObject(self.editor)
        self.animy.setPropertyName("y".encode("utf-8"))
        self.animationgroup.addAnimation(self.animy)
        self.animw = QPropertyAnimation()
        self.animw.setDuration(300)
        self.animw.setStartValue(self.sourcewidget.size().width())
        self.animw.setEndValue(self.size().width())
        self.animw.setTargetObject(self.editor)
        self.animw.setPropertyName("width".encode("utf-8"))
        self.animationgroup.addAnimation(self.animw)
        self.animh = QPropertyAnimation()
        self.animh.setDuration(300)
        self.animh.setStartValue(self.sourcewidget.size().height())
        self.animh.setEndValue(self.size().height())
        self.animh.setTargetObject(self.editor)
        self.animh.setPropertyName("height".encode("utf-8"))
        self.animationgroup.addAnimation(self.animh)
        self.animationgroup.finished.connect(self.animationFineshedZoomIn)
        self.animationgroup.start()

    def animationFineshedZoomIn(self):
        pass

    def editorClosed(self):
        pos = self.sourcewidget.mapTo(self, QPoint(0,0))
        # correct end values in case of resizing the window
        self.animx.setStartValue(pos.x())
        self.animy.setStartValue(pos.y())
        self.animw.setStartValue(self.sourcewidget.size().width())
        self.animh.setStartValue(self.sourcewidget.size().height())
        self.animationgroup.setDirection(QAbstractAnimation.Backward)
        #self.animationgroup.finished()), this, SLOT(animationFineshedZoomIn()));
        #connect(m_animationgroup, SIGNAL(finished()), this, SLOT(animationFineshedZoomOut()));
        self.animationgroup.start()

        item = self.list.item(self.row, 1)
        item.setData(Qt.UserRole, self.editor.slide)
        item.setText(self.editor.slide.title)
        if self.editor.changed:
            self.contentChanged()

    def animationFineshedZoomOut(self):
        #delete m_animationgroup
        #delete m_editor
        #self.editor = None
        pass

    def deleteSlide(self, slide):
        for row in range(self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == slide:
                self.list.removeRow(row)
                self.contentChanged()
                break

    def editSlide(self, slide):
        for row in range(self.list.rowCount()):
            item = self.list.item(row, 1)
            m = item.data(Qt.UserRole)
            if m == slide:
                self.list.selectRow(row)
                self.tableDoubleClicked(row)
                break


class Slide(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "Slide"
        self._src = ""
        self._title = ""

    @Property('QString')
    def src(self):
        return self._src
    
    @src.setter
    def src(self, src):
        self._src = src

    @Property('QString')
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title

    def getHtml(self):
        return ""
    
    def save(self, indent):
        qml = "\n"
        qml += " " * indent + "Slide {\n"
        qml += self.getAttributeQml(indent + 4, "id", self._id)
        qml += self.getAttributeQml(indent + 4, "src", self._src)
        qml += self.getAttributeQml(indent + 4, "text", self._text)
        qml += " " * indent + "}\n"
        return qml

@ClassInfo(DefaultProperty = 'items')
class Carousel(Item):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tag_name = "Carousel"
        self.display_name = QCoreApplication.translate("CarouselEditor", "Carousel")
        self._src = ""
        self._id = ""
        self._items = []

    def item(self, n):
        return self._items[n]

    def itemCount(self):
        return len(self._items)

    def appendItem(self, item):
        self._items.append(item)

    items = ListProperty(Item, appendItem)

    @Property('QString')
    def src(self):
        return self._src

    @src.setter
    def src(self, src):
        self._src = src

    @Property('QString')
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def getQml(self, indent):
        qml = "\n"
        qml += " " * indent + "Carousel {\n"
        qml += self.getAttributeQml(indent + 4, "id", self._id)
        qml += self.getAttributeQml(indent + 4, "src", self._src)
        qml += self.getAttributeQml(indent + 4, "text", self._text)
        qml += self.getAttributeQml(indent + 4, "adminlabel", self._adminlabel)
        qml += " " * indent + "}\n"
        return qml

    def getHtml(self):
        #QHash<QString,QString> attributes
        #QStringList urls
        #QStringList inner
        id = "main-carousel"

        #foreach(QXmlStreamAttribute att, xml.attributes())
        #{
        #    QString attName = att.name().toString()
        #    QString value = att.value().toString()
        #    if(attName == "adminlabel")
        #         // ignore
        #    else if(attName == "id")
        #    {
        #        if(!value.isEmpty())
        #            id = value
        #    }
        #    else
        #        attributes.insert(attName, value)
        #}

        html = "<div id=\"" + id + "\" class=\"carousel slide\" data-ride=\"carousel\">\n"
        html += "<ol class=\"carousel-indicators\">\n"

        #while(xml.readNext())
        #{
        #    if(xml.isStartElement() && xml.name() == "Slide")
        #    {
        #        QString source = xml.attributes().value("src").toString()
        #        QString url = source.mid(source.indexOf("assets/images/"))
        #        urls.append(url)

        #        inner.append(xml.readElementText())
        #    }
        #    else if(xml.isEndElement() && xml.name() == "Slider")
        #        break
        #}

        #int pos = 0
        #foreach(QString url, urls)
        #{
        #    html += "<li data-target=\"#" + id + "\" data-slide-to=\"" + QString.number(pos) + "\"" + (pos == 0 ? " class=\"active\"" : "") + "></li>\n"
        #    pos++
        #}
        html += "</ol>\n"
        html += "<div class=\"carousel-inner\">\n"

        #pos = 0
        #foreach(QString url, urls)
        #{
        #    html += "<div class=\"item"
        #    if(pos == 0)
        #        html += " active"
        #    html += "\" "
        #    foreach(QString attName, attributes.keys())
        #    {
        #        html += " " + attName + "=\"" + attributes.value(attName) + "\""
        #    }
        #    html += ">\n"
        #    html += "<img src=\"" + url + "\" style=\"width:100%\">\n"
        #    html += inner.at(pos) + "\n"
        #    html += "</div>\n"
        #    pos++
        #}
        html += "</div>\n"
        html += "<a class=\"left carousel-control\" href=\"#" + id + "\" data-slide=\"prev\">\n"
        html += "<span class=\"glyphicon glyphicon-chevron-left\"></span>\n"
        html += "<span class=\"sr-only\">Previous</span>\n"
        html += "</a>\n"
        html += "<a class=\"right carousel-control\" href=\"#" + id + "\" data-slide=\"next\">\n"
        html += "<span class=\"glyphicon glyphicon-chevron-right\"></span>\n"
        html += "<span class=\"sr-only\">Next</span>\n"
        html += "</a>\n"
        html += "</div>\n"
        return html


class SlideEditor(AnimateableEditor):

    def __init__(self):
        super().__init__()
        self.changed = False
        self.setAutoFillBackground(True)

        grid = QGridLayout()

        seek = QPushButton("...")
        seek.setMaximumWidth(50)
        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)
        titleLabel = QLabel(QCoreApplication.translate("CarouselEditor", "Slide"))
        fnt = titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        titleLabel.setFont(fnt)
        self.source = QLineEdit()
        self.image = ImageSelector()
        self.image.setImage(QImage(":/images/image_placeholder.png"))

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip(QCoreApplication.translate("general", "Close Editor"))

        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(13)
        self.innerHtml = QTextEdit()
        self.innerHtml.setMaximumHeight(120)
        self.innerHtml.setFont(font)
        self.innerHtml.setAcceptRichText(False)
        self.innerHtml.setLineWrapMode(QTextEdit.NoWrap)
        metrics = QFontMetrics(font)
        #self.innerHtml.setTabStopWidth(4 * metrics.width(' '))
        XmlHighlighter(self.innerHtml.document())

        grid.addWidget(titleLabel, 0, 0)
        grid.addWidget(close, 0, 2, 1, 1, Qt.AlignRight)
        grid.addWidget(QLabel(QCoreApplication.translate("CarouselEditor", "Path")), 1, 0)
        grid.addWidget(self.source, 2, 0, 1, 2)
        grid.addWidget(seek, 2, 2)
        grid.addWidget(self.image, 3, 0, 1, 2)
        grid.setRowStretch(3, 1)
        grid.addWidget(QLabel(QCoreApplication.translate("CarouselEditor", "Inner HTML")), 4, 0)
        grid.addWidget(self.innerHtml, 5, 0, 1, 3)
        grid.addWidget(QLabel(QCoreApplication.translate("general", "Admin Label")), 6, 0)
        grid.addWidget(self.adminlabel, 7, 0)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        #connect(self.image, SIGNAL(clicked()), this, SLOT(seek()))
        #connect(seek, SIGNAL(clicked(bool)), this, SLOT(seek()))
        #connect(self.source, SIGNAL(textChanged(QString)), this, SLOT(contentChanged()))
        #connect(self.adminlabel, SIGNAL(textChanged(QString)), this, SLOT(contentChanged()))
        #connect(self.innerHtml, SIGNAL(textChanged()), this, SLOT(contentChanged()))

    def setSlide(self, slide):
        self.slide = slide
        self.source.setText(slide.src)
        if slide.src:
            self.image.setImage(QImage(slide.src))
        else:
            self.image.setImage(QImage(":/images/image_placeholder.png"))
        self.innerHtml.setPlainText(slide._text)
        self.adminlabel.setText(slide._adminlabel)
        self.changed = False

    def closeEditor(self):
        if self.changed:
            self.slide.setSource(self.source.text())
            self.slide.setInnerHtml(self.innerHtml.toPlainText())
            self.slide.setAdminLabel(self.adminlabel.text())
        self.closes.emit()