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
        self.setStyleSheet("QLabel, QPushButton, QComboBox {font: 10pt}")
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.i = 0
        self.lock_flag = True
        self.setWindowTitle('ssPyQt5')
        self.count_label = QLabel(f'Нажатий:', self)
        self.shops_combo = QComboBox(self)
        self.operators_combo = QComboBox(self)
        self.passage_combo = QComboBox(self)
        self.lock_button = QPushButton(self)
        self.copy_login_button = QPushButton(self)
        self.copy_password_button = QPushButton(self)
        self.main_button = QPushButton('Открыть камеру', self)
        self.main_button.setEnabled(False)
        self.work_dir = ''
        self.count_mode = 0
        self.work_dir_label = QLabel('Рабочая директория: ', self)
        self.save_status = QLabel('', self)
        self.save_status.setGeometry(20, 120, 270, 40)
        self.time_label = QLabel(self)
        self.time_label.setText('Разница во времени с Москвой:')
        self.time_difference = 0
        self.login_label = QLabel(self)
        self.login_value = 'login'
        self.password_label = QLabel(self)
        self.password_value = 'password'
        self.clipboard = QtWidgets.QApplication.clipboard()
        # главное окно
        # отступ от левого края / отступ сверху / длина / высота
        self.setGeometry(300, 700, 1050, 200)
        self.UiComponents()
        self.show()

    def UiComponents(self):
        # кнопка счётчика
        # отступ от левого края / отступ сверху / длина / высота
        self.main_button.setGeometry(120, 30, 120, 40)
        self.main_button.clicked.connect(self.clickme)
        # лейбл кнопки счетчика
        button_label = QLabel(self)
        button_label.setText(
            'Нажмите на кнопку\n    или на пробел')
        button_label.setGeometry(120, 70, 200, 40)
        # лейбл значения счётчика
        self.count_label.setGeometry(20, 30, 100, 40)

        # кнопка блокировки
        # отступ от левого края / отступ сверху / длина / высота
        self.lock_button.setGeometry(910, 75, 35, 35)
        self.lock_button.setStyleSheet('background-image : url(lock.png);')
        self.lock_button.clicked.connect(self.lock)

        # кнопка копирования логина
        # отступ от левого края / отступ сверху / длина / высота
        self.copy_login_button.setGeometry(500, 25, 35, 35)
        self.copy_login_button.setStyleSheet(
            'background-image : url(copy.png);')
        self.copy_login_button.clicked.connect(self.copy_login)
        self.login_label.setText('Логин: ')
        self.login_label.setGeometry(350, 25, 140, 35)

        # кнопка копирования пароля
        # отступ от левого края / отступ сверху / длина / высота
        self.copy_password_button.setGeometry(500, 75, 35, 35)
        self.copy_password_button.setStyleSheet(
            'background-image : url(copy.png);')
        self.copy_password_button.clicked.connect(self.copy_password)
        self.password_label.setText('Пароль: ')
        self.password_label.setGeometry(350, 75, 140, 35)

        # список магазинов
        shops = model.get_shops()
        for shop in shops:
            self.shops_combo.addItem(shop)
        self.shops_combo.resize(200, 30)
        self.shops_combo.move(690, 55)

        shops_label = QLabel(self)
        shops_label.setText('Магазин:')
        shops_label.move(620, 55)

        # список операторов
        operators = model.get_operators()
        for operator in operators:
            self.operators_combo.addItem(operator)
        self.operators_combo.resize(200, 30)
        self.operators_combo.move(690, 15)

        operators_label = QLabel(self)
        operators_label.setText('Оператор:')
        operators_label.move(620, 15)

        # список проходов
        for i in range(1, 6):
            self.passage_combo.addItem(str(i))
        self.passage_combo.resize(200, 30)
        self.passage_combo.move(690, 95)

        passage_label = QLabel(self)
        passage_label.setText('Проход:')
        passage_label.move(620, 95)

        # разница во времени
        self.time_label.resize(200, 30)
        self.time_label.move(620, 135)

        # рабочая директория
        self.work_dir_label.move(50, 170)
        self.work_dir_label.resize(600, 30)

    def clickme(self):
        if self.count_mode == 2:
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
        elif self.count_mode == 0:
            model.open_camera('172.16.31.103')
            self.main_button.setText('Начать')
            self.count_mode = 1
        else:
            self.count_mode = 2
            self.main_button.setText('Считать')

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
            self.login_label.setText(f'Логин: {self.login_value}')
            self.password_label.setText(f'Пароль: {self.password_value}')
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
            self.main_button.setText('Открыть камеру')
            self.lock_flag = True
            self.count_mode = 0

    def copy_login(self):
        self.clipboard.setText(self.login_value)

    def copy_password(self):
        self.clipboard.setText(self.password_value)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
