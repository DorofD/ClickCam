from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(0, 0, 600, 150)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):

        # creating a push button
        button = QPushButton("CLICK", self)

        # setting geometry of button
        button.setGeometry(100, 10, 100, 40)

        # setting name
        button.setAccessibleName("push button")

        # adding action to a button
        button.clicked.connect(self.clickme)

        # accessing the name of button
        name = button.accessibleName()

        # creating a label to display a name
        label = QLabel(self)
        label.setText(name)
        label.move(200, 200)

    # action method
    def clickme(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, 0, 0, -1, -1)
        now = datetime.datetime.now()
        time = (str(now).replace(':', '.'))
        screenshot.save(f'screenshots\{time}.jpg', 'jpg')
        # printing pressed
        # pyscreenshot.grab().save(f"sas.png")
        print("pressed")
        # image.save(f"{time}.png")

        # create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())


# from PyQt5 import QtWidgets
# import sys

# app = QtWidgets.QApplication(sys.argv)
# w = QtWidgets.QWidget()

# grab_btn = QtWidgets.QPushButton('Grab Screen')


# def click_handler():
#     screen = QtWidgets.QApplication.primaryScreen()
#     screenshot = screen.grabWindow(0, 0, 0, 1000, 1000)
#     screenshot.save('shot.jpg', 'jpg')
#     # w.close()


# grab_btn.clicked.connect(click_handler)

# layout = QtWidgets.QVBoxLayout()
# layout.addWidget(grab_btn)
# w.setLayout(layout)
# w.show()

# sys.exit(app.exec_())
