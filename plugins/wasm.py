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
import os
import stat
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
from PySide6.QtWidgets import QHBoxLayout, QTextEdit, QVBoxLayout, QComboBox, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, QScrollArea
from PySide6.QtCore import Qt, QUrl, Signal, QDir, QFile, QAbstractListModel, QModelIndex, Property
from PySide6.QtGui import QFont, QFontMetrics, QImage, QSyntaxHighlighter, QTextCharFormat, QColor, QUndoStack
from PySide6.QtQml import qmlRegisterType
import plugins.wasm_rc

 
class WasmEditor(ElementEditorInterface):
    close = Signal()

    def __init__(self):
        ElementEditorInterface.__init__(self)
        self.site = None
        self.class_name = "WebAssemblyEditor"
        self.display_name = "Wasm"
        self.tag_name = "Wasm"
        self.version = "1.0"
        self.icon = QImage(":/wasm.svg")
        self.changed = False
        self.setAutoFillBackground(True)

        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(15)

        grid = QGridLayout()

        close = FlatButton(":/images/close_normal.png", ":/images/close_hover.png")
        close.setToolTip("Close Editor")

        self.url = QLineEdit()
        self.theme = QComboBox()
        self.theme.addItem("Light", "0")
        self.theme.addItem("Dark", "1")
        self.theme.addItem("System", "2")

        self.primary = QComboBox()
        self.primary.setEditable(True)
        self.primary.currentTextChanged.connect(self.primary_text_changed)
        self.primary.setModel(MaterialColorListModel())
      
        self.accent = QComboBox()
        self.accent.setEditable(True)
        self.accent.currentTextChanged.connect(self.accent_text_changed)
        self.accent.setModel(MaterialColorListModel())
        
        self.foreground = QComboBox()
        self.foreground.setEditable(True)
        self.foreground.currentTextChanged.connect(self.foreground_text_changed)
        self.foreground.setModel(MaterialColorListModel())
      
        self.background = QComboBox()
        self.background.setEditable(True)
        self.background.currentTextChanged.connect(self.background_text_changed)
        self.background.setModel(MaterialColorListModel())

        self.adminlabel = QLineEdit()
        self.adminlabel.setMaximumWidth(200)

        self.titleLabel = QLabel("Wasm Module")
        fnt = self.titleLabel.font()
        fnt.setPointSize(16)
        fnt.setBold(True)
        self.titleLabel.setFont(fnt)

        grid.addWidget(self.titleLabel, 0, 0)
        grid.addWidget(close, 0, 1, 1, 1, Qt.AlignRight)
        grid.addWidget(QLabel("Content.Url"), 1, 0)
        grid.addWidget(self.url, 2, 0, 1, 2)
        grid.addWidget(QLabel("Material.Theme"), 3, 0)
        grid.addWidget(self.theme, 4, 0)
        grid.addWidget(QLabel("Material.Primary"), 5, 0)
        grid.addWidget(self.primary, 6, 0)
        grid.addWidget(QLabel("Material.Accent"), 7, 0)
        grid.addWidget(self.accent, 8, 0)
        grid.addWidget(QLabel("Material.Foreground"), 9, 0)
        grid.addWidget(self.foreground, 10, 0)
        grid.addWidget(QLabel("Material.Background"), 11, 0)
        grid.addWidget(self.background, 12, 0)
        grid.addWidget(QLabel("Admin Label"), 13, 0)
        grid.addWidget(self.adminlabel, 14, 0, 1, 2)
        self.setLayout(grid)

        close.clicked.connect(self.closeEditor)
        self.url.textChanged.connect(self.contentChanged)
        self.adminlabel.textChanged.connect(self.contentChanged)
        self.theme.currentTextChanged.connect(self.contentChanged)

    def primary_text_changed(self, s):
        self.changeBg(self.primary, s)

    def accent_text_changed(self, s):
        self.changeBg(self.accent, s)

    def foreground_text_changed(self, s):
        self.changeBg(self.foreground, s)

    def background_text_changed(self, s):
        self.changeBg(self.background, s)

    def changeBg(self, cb, s):
        c = QColor(s)
        if(c.isValid()):
            cb.setStyleSheet("background-color: " + s + " ;")
        self.contentChanged()

    def setCaption(self, caption):
        self.titleLabel.setText(caption)

    def setText(self, text):
        self.url.setText(text)

    def getText(self):
        return self.url.text()

    def setContent(self, content):
        self.content = content
        if content:
            if isinstance(content, Wasm):
                self.adminlabel.setText(content.adminlabel)
                self.url.setText(content.text)
                self.theme.setCurrentIndex(int(content.theme))
                self.foreground.setCurrentText(content.foreground)
                self.background.setCurrentText(content.background)
                self.primary.setCurrentText(content.primary)
                self.accent.setCurrentText(content.accent)
            else:
                self.url.setText(content.text)
                self.adminlabel.setText(content.adminlabel)
            self.changed = False

    def getContent(self):
        return self.content

    def getDefaultContent(self):
        return Wasm()

    def setSite(self, site):
        self.site = site

    def closeEditor(self):
        if self.changed:
            if self.content:
                self.content.adminlabel = self.adminlabel.text()
                self.content.text = self.url.text()
                self.content.theme = str(self.theme.currentIndex())
                self.content.foreground = self.foreground.currentText()
                self.content.background = self.background.currentText()
                self.content.primary = self.primary.currentText()
                self.content.accent = self.accent.currentText()

        self.close.emit()

    def registerContenType(self):
        qmlRegisterType(Wasm, 'WasmEditor', 1, 0, 'Wasm')

    def pluginScripts(self):
        script = ""
        return script

    def getImportString(self):
        return "import WasmEditor 1.0\n"

    def installAssets(self, assets_path):
        assets = QDir(assets_path)
        assets.mkdir("plugins")
        assets.cd("plugins")
        assets.mkdir("wasm")

        dst = os.path.join(assets_path, "plugins", "wasm", "wasm.svg")
        QFile.copy(":/wasm.svg", dst)
        os.chmod(dst, stat.S_IWRITE | stat.S_IREAD | stat.S_IWGRP | stat.S_IRGRP | stat.S_IROTH)

        dst = os.path.join(assets_path, "plugins", "wasm", "qtloader.js")
        QFile.copy(":/qtloader.js", dst)
        os.chmod(dst, stat.S_IWRITE | stat.S_IREAD | stat.S_IWGRP | stat.S_IRGRP | stat.S_IROTH)

        dst = os.path.join(assets_path, "plugins", "wasm", "appqmlwasm.wasm")
        QFile.copy(":/appqmlwasm.wasm", dst)
        os.chmod(dst, stat.S_IWRITE | stat.S_IREAD | stat.S_IWGRP | stat.S_IRGRP | stat.S_IROTH)

        dst = os.path.join(assets_path, "plugins", "wasm", "appqmlwasm.js")
        QFile.copy(":/appqmlwasm.js", dst)
        os.chmod(dst, stat.S_IWRITE | stat.S_IREAD | stat.S_IWGRP | stat.S_IRGRP | stat.S_IROTH)


class Wasm(Item):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_name = "Wasm"
        self._theme = ""
        self._foreground = ""
        self._background = ""
        self._primary = ""
        self._accent = ""

    @Property('QString')
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, theme):
        self._theme = theme

    @Property('QString')
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, foreground):
        self._foreground = foreground

    @Property('QString')
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = background

    @Property('QString')
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, primary):
        self._primary = primary

    @Property('QString')
    def accent(self):
        return self._accent

    @accent.setter
    def accent(self, accent):
        self._accent = accent

    def clone(self):
        txt = Wasm()
        txt.id = self._id
        txt.text = self._text   
        txt.adminlabel = self._adminlabel
        return txt

    def getHtml(self):
        f = open("plugins\wasm_snippet.html", "r")
        content = f.read()
        f.close()

        content = content.replace("{{contenUrl}}", "\"" + self._text + "\"")
        content = content.replace("{{theme}}", "\"" + self._theme + "\"")
        content = content.replace("{{foreground}}", "\"" + self._foreground + "\"")
        content = content.replace("{{background}}", "\"" + self._background + "\"")
        content = content.replace("{{primary}}", "\"" + self._primary + "\"")
        content = content.replace("{{accent}}", "\""+ self._accent + "\"")
        return html.unescape(content)

    def getQml(self, indent):
        qml = "\n"
        qml += " " * indent + "Wasm {\n"
        qml += self.getAttributeQml(indent + 4, "id", self._id)
        qml += self.getAttributeQml(indent + 4, "text", self._text)
        qml += self.getAttributeQml(indent + 4, "theme", self._theme)
        qml += self.getAttributeQml(indent + 4, "foreground", self._foreground)
        qml += self.getAttributeQml(indent + 4, "background", self._background)
        qml += self.getAttributeQml(indent + 4, "primary", self._primary)
        qml += self.getAttributeQml(indent + 4, "accent", self._accent)

        qml += self.getAttributeQml(indent + 4, "adminlabel", self._adminlabel)
        qml += " " * indent + "}\n"
        return qml


class MaterialColorListModel(QAbstractListModel):
    def __init__(self):
        QAbstractListModel.__init__(self)
        self.colors = []
        # light
        self.colors.append(["Red", "#F44336"])
        self.colors.append(["Pink (default accent)", "#E91E63"])
        self.colors.append(["Purple", "#9C27B0"])
        self.colors.append(["DeepPurple", "#673AB7"])
        self.colors.append(["Indigo (default primary)", "#3F51B5"])
        self.colors.append(["Blue", "#2196F3"])
        self.colors.append(["LightBlue", "#03A9F4"])
        self.colors.append(["Cyan", "#00BCD4"])
        self.colors.append(["Teal", "#009688"]) 
        self.colors.append(["Green", "#4CAF50"]) 
        self.colors.append(["LightGreen", "#8BC34A"]) 
        self.colors.append(["Lime", "#CDDC39"]) 
        self.colors.append(["Yellow", "#FFEB3B"]) 
        self.colors.append(["Amber", "#FFC107"])
        self.colors.append(["Orange", "#FF9800"]) 
        self.colors.append(["DeepOrange", "#FF5722"]) 
        self.colors.append(["Brown", "#795548"]) 
        self.colors.append(["Gray", "#9E9E9E"]) 
        self.colors.append(["BlueGray", "#607D8B"])  
        #dark
        self.colors.append(["Red", "#EF9A9A"])
        self.colors.append(["Pink (default accent)", "#F48FB1"])
        self.colors.append(["Purple", "#CE93D8"])
        self.colors.append(["DeepPurple", "#B39DDB"])
        self.colors.append(["Indigo (default primary)", "#9FA8DA"])
        self.colors.append(["Blue", "#90CAF9"])
        self.colors.append(["LightBlue", "#81D4FA"])
        self.colors.append(["Cyan", "#80DEEA"])
        self.colors.append(["Teal", "#80CBC4"]) 
        self.colors.append(["Green", "#A5D6A7"]) 
        self.colors.append(["LightGreen", "#C5E1A5"]) 
        self.colors.append(["Lime", "#E6EE9C"]) 
        self.colors.append(["Yellow", "#FFF59D"]) 
        self.colors.append(["Amber", "#FFE082"])
        self.colors.append(["Orange", "#FFCC80"]) 
        self.colors.append(["DeepOrange", "#FFAB91"]) 
        self.colors.append(["Brown", "#BCAAA4"]) 
        self.colors.append(["Gray", "#EEEEEE"]) 
        self.colors.append(["BlueGray", "#B0BEC5"])  

    def rowCount(self, parent:QModelIndex=...):
        return len(self.colors)

    def data(self, index:QModelIndex, role:int=...):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self.colors[index.row()][0]
        elif role == Qt.EditRole:
            return self.colors[index.row()][1]
        elif role == 8:
            return QColor(self.colors[index.row()][1])
        return None
