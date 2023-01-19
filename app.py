from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import model
# pyinstaller main.spec


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.lock_flag = True
        self.setWindowTitle("ssPyQt5")
        self.count_label = QLabel(f'Нажатий:', self)
        # отступ от левого края / отступ сверху / длина / высота
        self.count_label.setGeometry(20, 30, 100, 40)
        self.shops_combo = QComboBox(self)
        self.operators_combo = QComboBox(self)
        self.passage_combo = QComboBox(self)
        self.lock_button = QPushButton(self)
        self.main_button = QPushButton("Нажать!", self)
        self.main_button.setEnabled(False)
        self.work_dir = ''
        self.work_dir_label = QLabel('Рабочая директория: ', self)
        self.save_status = QLabel('', self)
        self.save_status.setGeometry(20, 120, 270, 40)
        self.time_label = QLabel(self)
        self.time_label.setText('Разница во времени с Москвой:')
        self.time_difference = 0
        # главное окно
        # отступ от левого края / отступ сверху / длина / высота
        self.setGeometry(300, 700, 650, 200)
        self.UiComponents()
        self.show()

    def UiComponents(self):
        # отступ от левого края / отступ сверху / длина / высота
        self.main_button.setGeometry(120, 30, 100, 40)
        self.main_button.clicked.connect(self.clickme)

        # кнопка блокировки
        # отступ от левого края / отступ сверху / длина / высота
        self.lock_button.setGeometry(580, 75, 35, 35)
        self.lock_button.setStyleSheet("background-image : url(lock.png);")
        self.lock_button.clicked.connect(self.lock)

        button_label = QLabel(self)
        button_label.setText(
            'Нажмите на кнопку\n    или на пробел')
        button_label.move(120, 70)

        # список магазинов
        shops = model.get_shops()
        for shop in shops:
            self.shops_combo.addItem(shop)
        self.shops_combo.resize(200, 30)
        self.shops_combo.move(360, 55)

        shops_label = QLabel(self)
        shops_label.setText('Магазин:')
        shops_label.move(300, 55)

        # список операторов
        operators = model.get_operators()
        for operator in operators:
            self.operators_combo.addItem(operator)
        self.operators_combo.resize(200, 30)
        self.operators_combo.move(360, 15)

        operators_label = QLabel(self)
        operators_label.setText('Оператор:')
        operators_label.move(300, 15)

        # список проходов
        for i in range(1, 7):
            self.passage_combo.addItem(str(i))
        self.passage_combo.resize(200, 30)
        self.passage_combo.move(360, 95)

        passage_label = QLabel(self)
        passage_label.setText('Проход:')
        passage_label.move(300, 95)

        # разница во времени
        self.time_label.resize(200, 30)
        self.time_label.move(300, 135)

        # рабочая директория
        self.work_dir_label.move(50, 170)
        self.work_dir_label.resize(600, 30)

    def clickme(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, 0, 0, -1, -1)
        if not screenshot.save(model.make_screenshot_name(self.work_dir,
                                                          self.time_difference,
                                                          self.operators_combo.currentText(),
                                                          self.shops_combo.currentText(),
                                                          self.passage_combo.currentText()), 'jpg'):
            self.save_status.setText(
                'Ошибка сохранения! Обратитесь к администратору')
            self.save_status.setStyleSheet('background-color: red')
        self.i += 1
        self.count_label.setText(f'Нажатий: {self.i}')

    def lock(self):
        if self.lock_flag:
            # активация кнопки счетчика
            self.main_button.setEnabled(True)
            # деактивация кнопок меню настроек
            self.shops_combo.setEnabled(False)
            self.operators_combo.setEnabled(False)
            self.passage_combo.setEnabled(False)
            self.lock_flag = False
            self.work_dir = model.make_directory(self.operators_combo.currentText(),
                                                 self.shops_combo.currentText(),
                                                 self.passage_combo.currentText())
            self.time_difference = model.find_time_difference(
                self.shops_combo.currentText())

            self.time_label.setText(
                f'Разница во времени с Москвой: {self.time_difference}')
            self.work_dir_label.setText(f'Рабочая директория: {self.work_dir}')
        else:
            # деактивация кнопки счетчика
            self.main_button.setEnabled(False)
            # активация кнопок меню настроек
            self.shops_combo.setEnabled(True)
            self.operators_combo.setEnabled(True)
            self.passage_combo.setEnabled(True)
            self.lock_flag = True


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
