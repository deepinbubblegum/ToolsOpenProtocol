from functools import cached_property
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class Page(QtWidgets.QWidget):
    completeChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.container)
        lay.addWidget(self.button, alignment=QtCore.Qt.AlignCenter)

        self.button.clicked.connect(self.handle_clicked)

    @cached_property
    def container(self):
        return QtWidgets.QWidget()

    @cached_property
    def button(self):
        return QtWidgets.QPushButton("Save")

    def handle_clicked(self):
        if self.validate():
            self.completeChanged.emit()

    def validate(self):
        # Override this method if you want to validate the entries, 
        # if it returns True then it will go to the next page, 
        # otherwise it will not move from the page
        return True


class TabWizard(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabBar().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.tabBar() and event.type() == QtCore.QEvent.MouseButtonPress:
            return True
        return super().eventFilter(obj, event)

    def addPage(self, page, title):
        if not isinstance(page, Page):
            raise TypeError(f"{page} must be Page object")
        self.addTab(page, title)
        page.completeChanged.connect(self.nextPage)

    def nextPage(self):
        next_index = self.currentIndex() + 1
        if next_index < self.count():
            self.setCurrentIndex(next_index)


class Page1(Page):
    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QtWidgets.QFormLayout(self.container)
        lay.addRow("Foo1", QtWidgets.QLineEdit())
        lay.addRow("Bar1", QtWidgets.QLineEdit())


class Page2(Page):
    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QtWidgets.QFormLayout(self.container)
        lay.addRow("Foo2", QtWidgets.QLineEdit())
        lay.addRow("Bar2", QtWidgets.QLineEdit())


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        tabwizard = TabWizard()
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(tabwizard)

        tabwizard.addPage(Page1(), "page1")
        tabwizard.addPage(Page2(), "page2")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())