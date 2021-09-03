import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import * 
from qt_material import apply_stylesheet

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
        
        # showing all the widgets
        self.show()
        
    # method for widgets
    def UiComponents(self):
        # creating label
        label = QLabel("Label", self)
  
        # setting geometry to label
        label.setGeometry(100, 100, 120, 40)
  
        # adding border to label
        label.setStyleSheet(
            "border : 1px solid black;"
            "border-radius: 8px"
        )
  
        # opening window in maximized size
        # self.showMaximized()
        
print(__name__)
     
def main():
# try:
    # create the application and the main window
    print('bca')
    app = QApplication(sys.argv)
    window = Window()
    apply_stylesheet(app, theme='dark_blue.xml')
    
    # # run
    # window.show()
# finally:
    # start the app
    sys.exit(app.exec())
        
if __name__ == '__main__':
    main()