from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime
# pyinstaller main.spec
i = 0


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("ssPyQt5")
        self.count_label = QLabel(f'Нажатий: {i}', self)
        self.count_label.setGeometry(50, 30, 100, 40)
        # setting geometry
        self.setGeometry(0, 0, 600, 100)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets

    def UiComponents(self):
        global i
        # count_label = QLabel("My text")
        # count_label = QLabel(f'Нажатий: {i}', self)
        # count_label.setGeometry(50, 30, 100, 40)
        # creating a push button
        button = QPushButton("Нажать!", self)

        # setting geometry of button
        button.setGeometry(250, 30, 100, 40)

        # setting name
        # button.setAccessibleName("button")

        # adding action to a button
        button.clicked.connect(self.clickme)

        # accessing the name of button
        name = button.accessibleName()

        # creating a count_label to display a name
        button_label = QLabel(self)
        button_label.setText(
            'Нажмите на кнопку\n    или на пробел')
        button_label.move(250, 70)

    # action method
    def clickme(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, 0, 0, -1, -1)
        now = datetime.datetime.now()
        time = (str(now).replace(':', '.'))
        screenshot.save(f'screenshots\{time}.jpg', 'jpg')
        # printing pressed
        # pyscreenshot.grab().save(f"sas.png")
        global i
        i += 1
        print("pressed")
        print(i)
        self.count_label.setText(f'Нажатий: {i}')
        # image.save(f"{time}.png")

        # create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
