# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
  
  
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # this will hide the title bar
        # self.setWindowFlag(Qt.FramelessWindowHint)
        
        # setting title
        self.setWindowTitle("GUI Manager")
  
        # setting geometry
        self.setGeometry(100, 100, 600, 400)
  
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
        label.setStyleSheet("border : 2px solid black; border-radius: 8px")
  
        # opening window in maximized size
        # self.showMaximized()
try:
    # create pyqt5 app
    App = QApplication(sys.argv)
    
    # create the instance of our Window
    window = Window()
    
finally:
    # start the app
    sys.exit(App.exec())