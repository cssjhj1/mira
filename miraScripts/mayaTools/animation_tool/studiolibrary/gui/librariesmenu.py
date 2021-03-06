#Embedded file name: C:/Users/hovel/Dropbox/packages/studiolibrary/1.23.2/build27/studiolibrary\gui\librariesmenu.py
import sys
import logging
from studioqt import QtGui
from studioqt import QtWidgets
import studioqt
import studiolibrary
__all__ = ['LibrariesMenu']
logger = logging.getLogger(__name__)

class LibrariesMenu(QtWidgets.QMenu):

    def __init__(self, *args):
        """
        """
        QtWidgets.QMenu.__init__(self, *args)
        self.setTitle('Libraries')
        self.reload()

    def reload(self):
        self.clear()
        for library in studiolibrary.libraries():
            action = LibraryAction(self, library)
            self.addAction(action)
            action.setStatusTip('Load library "%s" "%s"' % (library.name(), library.path()))
            action.triggered.connect(library.load)


class LibraryAction(QtWidgets.QWidgetAction):
    STYLE_SHEET = '\n#actionIcon {\n    background-color: ACCENT_COLOR;\n}\n\n#actionWidget {\n    background-color: BACKGROUND_COLOR;\n}\n\n#actionLabel, #actionLabel, #actionOption {\n    background-color: BACKGROUND_COLOR;\n    color: rgb(255, 255, 255);\n}\n#actionLabel:hover, #actionLabel:hover, #actionOption:hover {\n    background-color: ACCENT_COLOR;\n    color: rgb(255, 255, 255);\n}\n'

    def __init__(self, parent, library):
        """
        :type parent: QtWidgets.QMenu
        :type library: studiolibrary.Library
        """
        QtWidgets.QWidgetAction.__init__(self, parent)
        self._library = library
        self.setText(self.library().name())

    def library(self):
        """
        :rtype: studiolibrary.Librarya
        """
        return self._library

    def deleteLibrary(self):
        """
        :rtype: None
        """
        self.parent().close()
        self.library().showDeleteDialog()

    def createWidget(self, parent):
        """
        :type parent: QtWidgets.QMenu
        """
        height = 25
        spacing = 1
        options = self.library().theme().options()
        styleSheet = studioqt.StyleSheet.fromText(LibraryAction.STYLE_SHEET, options=options)
        actionWidget = QtWidgets.QFrame(parent)
        actionWidget.setObjectName('actionWidget')
        actionWidget.setStyleSheet(styleSheet.data())
        actionLabel = QtWidgets.QLabel(self.library().name(), actionWidget)
        actionLabel.setObjectName('actionLabel')
        actionLabel.setFixedHeight(height)
        iconColor = QtGui.QColor(255, 255, 255, 220)
        icon = studiolibrary.resource().icon('delete', color=iconColor)
        actionOption = QtWidgets.QPushButton('', actionWidget)
        actionOption.setObjectName('actionOption')
        actionOption.setIcon(icon)
        actionOption.setFixedHeight(height + spacing)
        actionOption.setFixedWidth(height)
        actionOption.clicked.connect(self.deleteLibrary)
        actionIcon = QtWidgets.QLabel('', actionWidget)
        actionIcon.setObjectName('actionIcon')
        actionIcon.setFixedWidth(10)
        actionIcon.setFixedHeight(height)
        actionLayout = QtWidgets.QHBoxLayout(actionWidget)
        actionLayout.setSpacing(0)
        actionLayout.setContentsMargins(0, 0, 0, 0)
        actionLayout.addWidget(actionIcon, stretch=1)
        actionLayout.addWidget(actionLabel, stretch=1)
        actionLayout.addWidget(actionOption, stretch=1)
        return actionWidget


class Example(QtWidgets.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()
        menubar = self.menuBar()
        menu = LibrariesMenu('Libraries', menubar)
        menubar.addMenu(menu)
        self.statusBar()
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Menubar')
        self.show()


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(funcName)s: %(message)s', filemode='w')
    app = QtWidgets.QApplication(sys.argv)
    e = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
