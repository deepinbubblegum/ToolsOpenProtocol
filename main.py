import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from qt_material import apply_stylesheet
from userinterface.TabsPage import TabsWidget
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.setWindowTitle("GUI Manager")
        self.setGeometry(100, 100, 720, 480)
        self.setWindowIcon(QIcon('icons/qt.png'))

        # calling method
        self.UiComponents()
        
    # method for widgets
    def UiComponents(self):
        self.tabs_widget = TabsWidget(self)
        self.setCentralWidget(self.tabs_widget)
    

def handleVisibleChanged():
    if not QGuiApplication.inputMethod().isVisible():
        return
    for w in QGuiApplication.allWindows():
        if w.metaObject().className() == "QtVirtualKeyboard::InputView":
            keyboard = w.findChild(QObject, "keyboard")
            if keyboard is not None:
                r = w.geometry()
                r.moveTop(keyboard.property("y"))
                w.setMask(QRegion(r))
                return

def main():
# try:
    # create the application and the main window
    app = QApplication(sys.argv)
    QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)
    window = Window()
    apply_stylesheet(app, theme='dark_blue.xml')
    
    # # run
    window.showFullScreen()
# finally:
    # start the app
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()