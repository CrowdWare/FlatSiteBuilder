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

import html
from widgets.hyperlink import HyperLink
from widgets.flatbutton import FlatButton
from widgets.animateableeditor import AnimateableEditor
from widgets.section import Section
from widgets.pageeditor import PageEditor
from widgets.sectioneditor import SectionEditor
from widgets.roweditor import RowEditor
from widgets.columneditor import ColumnEditor
from widgets.elementeditor import ElementEditor, Mode
from widgets.content import ContentType
from widgets.interfaces import ElementEditorInterface
from widgets.item import Item
from PySide6.QtWidgets import  QHBoxLayout, QTextEdit, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PySide6.QtCore import Qt, QUrl, Signal,  QCoreApplication
from PySide6.QtGui import QFont, QFontMetrics, QImage, QSyntaxHighlighter, QTextCharFormat, QColor, QUndoStack
from PySide6.QtQml import qmlRegisterType
import plugins.texteditor_rc


class TextEditor(ElementEditorInterface):
    close = Signal()

    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.site = None
        self.class_name = "TextEditor"
        self.display_name = "Text"
        self.tag_name = "Text"
        self.version = "1.0"
        self.icon = QImage(":/texteditor.png")
        self.changed = False
        self.setAutoFillBackground(True)
        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(15)

        grid = QGridLayout()

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip(QCoreApplication.translate("general", "Close Editor"))
        self.html = QTextEdit()
        self.html.setFont(font)
        self.html.setAcceptRichText(False)
        self.html.setLineWrapMode(QTextEdit.NoWrap)
        metrics = QFontMetrics(font)
        self.html.setTabStopDistance(4 * metrics.horizontalAdvance(' '))

        self.highlighter = XmlHighlighter(self.html.document())

        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)

        self.titleLabel = QLabel(QCoreApplication.translate("TextEditor", "Text Module"))
        fnt = self.titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        self.titleLabel.setFont(fnt)

        grid.addWidget(self.titleLabel, 0, 0)
        grid.addWidget(close, 0, 1, 1, 1, Qt.AlignRight)
        grid.addWidget(self.html, 1, 0, 1, 2)
        grid.addWidget(QLabel(QCoreApplication.translate("TextEditor", "Admin Label")), 2, 0)
        grid.addWidget(self.adminlabel, 3, 0, 1, 2)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.html.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)

    def setCaption(self, caption):
        self.titleLabel.setText(caption)

    def setText(self, text):
        self.html.setPlainText(html.unescape(text))

    def getText(self):
            return html.escape(self.html.toPlainText())

    def getUnescapedText(self):
            return self.html.toPlainText()

    def setContent(self, content):
        self.content = content
        if content:
            if isinstance(content, Text):
                self.adminlabel.setText(content.adminlabel)
                self.html.setPlainText(html.unescape(content.text))
            else:
                self.html.setPlainText(html.unescape(content.text))
                self.adminlabel.setText(content.adminlabel)
            self.changed = False

    def getContent(self):
        return self.content

    def getDefaultContent(self):
        return Text()

    def setSite(self, site):
        self.site = site

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.adminlabel = self.adminlabel.text()
                self.content.text = html.escape(self.html.toPlainText())
        self.close.emit()

    def registerContenType(self):
        qmlRegisterType(Text, 'TextEditor', 1, 0, 'Text')

    def getImportString(self):
        return "import TextEditor 1.0\n"


class Text(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "Text"
        self.display_name = QCoreApplication.translate("TextEditor", "Text")

    def clone(self):
        txt = Text()
        txt.id = self._id
        txt.text = self._text
        txt.adminlabel = self._adminlabel
        return txt

    def getQml(self, indent):
        qml = "\n"
        qml += " " * indent + "Text {\n"
        qml += self.getAttributeQml(indent + 4, "id", self._id)
        qml += self.getAttributeQml(indent + 4, "text", self._text)
        qml += self.getAttributeQml(indent + 4, "adminlabel", self._adminlabel)
        qml += " " * indent + "}\n"
        return qml

    def getHtml(self):
        return html.unescape(self.text)


ENTITY = 0
TAG = 1
CODE = 2
COMMENT = 3
LAST_CONSTRUCT = COMMENT


NORMAL_STATE = -1
IN_COMMENT = 0
IN_TAG = 1
IN_VAR = 2
IN_LOOP = 3


class XmlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent = None):
        super(XmlHighlighter, self).__init__(parent)

        self.formats = [0] * (LAST_CONSTRUCT + 1)
        entityFormat = QTextCharFormat()
        entityFormat.setForeground(QColor(0, 128, 0))
        entityFormat.setFontWeight(QFont.Normal)
        self.setFormatFor(ENTITY, entityFormat)

        tagFormat = QTextCharFormat()
        tagFormat.setForeground(QColor("#f0e68c"))
        tagFormat.setFontWeight(QFont.Normal)
        self.setFormatFor(TAG, tagFormat)

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#87ceeb"))
        commentFormat.setFontItalic(True)
        self.setFormatFor(COMMENT, commentFormat)

        codeFormat = QTextCharFormat()
        codeFormat.setForeground(QColor("#ff9e00"))
        self.setFormatFor(CODE, codeFormat)

    def setFormatFor(self, construct, format):
        self.formats[construct] = format
        self.rehighlight()

    def formatFor(self, construct):
        return self.formats[construct]

    def highlightBlock(self, text):
        state = self.previousBlockState()
        length = len(text)
        start = 0
        pos = 0

        while pos < length:
            if state == IN_VAR:
                start = pos
                while pos < length:
                    if text[pos:pos + 2] == "":
                        pos += 2
                        state = NORMAL_STATE
                        break
                    else:
                        pos = pos + 1
                self.setFormat(start, pos - start, self.formats[CODE])

            elif state == IN_LOOP:
                start = pos
                while pos < length:
                    if text[pos: pos + 2] == "%":
                        pos += 2
                        state = NORMAL_STATE
                        break
                    else:
                        pos = pos + 1
                self.setFormat(start, pos - start, self.formats[CODE])

            elif state == IN_COMMENT:
                start = pos
                while pos < length:
                    if text[pos: pos + 3] == "-->":
                        pos += 3
                        state = NORMAL_STATE
                        break
                    else:
                        pos = pos + 1
                self.setFormat(start, pos - start, self.formats[COMMENT])

            elif state == IN_TAG:
                quote = 0
                start = pos
                while pos < length:
                    ch = text[pos]
                    if quote == 0:
                        if ch == "\"" or ch == '"':
                            quote = ch
                        elif ch == '>':
                            pos = pos + 1
                            state = NORMAL_STATE
                            break
                    elif ch == quote:
                        quote = 0
                    pos = pos + 1
                self.setFormat(start, pos - start, self.formats[TAG])

            else:
                while pos < length:
                    ch = text[pos]
                    if ch == '<':
                        if text[pos: pos + 4] == "<!--":
                            state = IN_COMMENT
                        else:
                            state = IN_TAG
                        break
                        
                    elif ch == '&':
                        start = pos
                        while pos < length and text[pos] != '':
                            pos = pos + 1
                                
                        self.setFormat(start, pos - start, self.formats[ENTITY])
                    elif ch == "":
                        if text[pos: pos + 2] == "":
                            state = IN_VAR
                            break
                        elif text[pos: pos + 2] == "%":
                            state = IN_LOOP
                            break
                        pos = pos + 1
                        break
                    else:
                        pos = pos +1

        self.setCurrentBlockState(state)
