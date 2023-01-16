from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import datetime
import dbscripts
# pyinstaller main.spec
i = 0


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("ssPyQt5")
        self.count_label = QLabel(f'Нажатий: {i}', self)
        # отступ от левого края / отступ сверху / длина / высота
        self.count_label.setGeometry(20, 30, 100, 40)
        self.shops_combo = QComboBox(self)
        self.operators_combo = QComboBox(self)

        # setting geometry
        # отступ от левого края / отступ сверху / длина / высота
        self.setGeometry(300, 700, 600, 100)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets

    def UiComponents(self):
        # creating a push button
        button = QPushButton("Нажать!", self)

        # setting geometry of button
        # отступ от левого края / отступ сверху / длина / высота
        button.setGeometry(120, 30, 100, 40)

        # adding action to a button
        button.clicked.connect(self.clickme)

        # creating a count_label to display a name
        button_label = QLabel(self)
        button_label.setText(
            'Нажмите на кнопку\n    или на пробел')
        button_label.move(120, 70)

        # список магазинов
        # shops_combo = QComboBox(self)
        self.shops_combo.addItem('Магазин 1')
        self.shops_combo.addItem('Магазин 2')
        self.shops_combo.addItem('Магазин 3')
        self.shops_combo.resize(200, 30)
        self.shops_combo.move(360, 15)

        shops_label = QLabel(self)
        shops_label.setText('Магазин:')
        shops_label.move(300, 15)

        # список операторов
        # operators_combo = QComboBox(self)
        self.operators_combo.addItem('Оператор 1')
        self.operators_combo.addItem('Оператор 2')
        self.operators_combo.addItem('Оператор 3')
        self.operators_combo.resize(200, 30)
        self.operators_combo.move(360, 55)

        operators_label = QLabel(self)
        operators_label.setText('Оператор:')
        operators_label.move(300, 55)

    def clickme(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, 0, 0, -1, -1)
        now = datetime.datetime.now()
        time = (str(now).replace(':', '.'))
        screenshot.save(f'screenshots\{time}.jpg', 'jpg')
        global i
        i += 1
        print("pressed")
        print(i)
        sas = self.shops_combo.currentText()
        self.count_label.setText(f'Нажатий: {i}')
        # image.save(f"{time}.png")


        # create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
