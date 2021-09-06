import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from qt_material import apply_stylesheet

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.setWindowTitle("GUI Manager")
        self.setGeometry(100, 100, 720, 480)
        self.setWindowIcon(QIcon('icons/qt.png'))
        
        # showing all the widgets
        # self.show()
        self.showFullScreen()
         
def main():
# try:
    # create the application and the main window
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme='dark_blue.xml')
    
    # # run
    window.showFullScreen()
# finally:
    # start the app
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()