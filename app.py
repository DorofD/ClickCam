from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import model
import time
# recorder
import pyautogui
import cv2
import numpy as np
import threading
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
        self.problem_button = QPushButton('Проблема с камерой', self)
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
        self.cam_address_label = QLabel(self)
        self.cam_address_label.setText('Камера: ')
        self.cam_address_value = ''
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.operator_input_password = QLineEdit(self)
        self.operator_input_password.setEchoMode(QLineEdit.Password)
        self.operator_value = model.get_operator()
        self.operators_label = QLabel(self)
        self.operators_label.setText(f'Оператор: {self.operator_value}')
        self.set_operator_button = QPushButton(self)
        self.problem_description = QLineEdit(self)
        self.problem_description.setPlaceholderText(
            'Проблема с камерой?')
        # таймер
        self.time = 0
        self.timeInterval = 1000  # 1 секунда

        self.timer_label = QLabel(self)
        self.timer = QTimer()
        self.timer.setInterval(self.timeInterval)
        self.timer.timeout.connect(self.updateUptime)
        self.recorder_up = True
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
        # лейбл значения счётчика нажатий
        self.count_label.setGeometry(20, 30, 100, 40)
        # лейбл таймера
        self.timer_label.setGeometry(20, 5, 220, 20)

        # кнопка проблемы с камерой
        # отступ от левого края / отступ сверху / длина / высота
        self.problem_button.setGeometry(50, 150, 210, 25)
        # (operator, time, address, problem_description)
        self.problem_button.clicked.connect(self.cam_problem_report)
        # описание проблемы
        self.problem_description.setGeometry(50, 120, 210, 25)
        self.problem_description.setMaxLength(50)

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

        # адрес камеры
        self.cam_address_label.setGeometry(350, 125, 140, 35)

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
        for i in range(1, 6):
            self.operators_combo.addItem(f'Оператор {i}')
        self.operators_combo.resize(100, 30)
        self.operators_combo.move(790, 15)

        self.operators_label.setGeometry(620, 15, 160, 30)
        # пароль для смены оператора
        self.operator_input_password.setGeometry(895, 15, 40, 30)
        # кнопка сохранения оператора
        self.set_operator_button.setGeometry(940, 12, 34, 34)
        self.set_operator_button.setStyleSheet(
            'background-image : url(set.png);')
        self.set_operator_button.clicked.connect(self.set_operator)

        # список проходов
        for i in range(1, 6):
            self.passage_combo.addItem(str(i))
        self.passage_combo.resize(200, 30)
        self.passage_combo.move(690, 95)

        passage_label = QLabel(self)
        passage_label.setText('Проход:')
        passage_label.move(620, 95)

        # разница во времени
        self.time_label.resize(210, 30)
        self.time_label.move(620, 135)

        # рабочая директория
        self.work_dir_label.move(350, 170)
        self.work_dir_label.resize(600, 30)

    def clickme(self):
        if self.count_mode == 2:
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow(0, 0, 0, -1, -1)
            if not screenshot.save(model.make_screenshot_name(self.work_dir,
                                                              self.time_difference,
                                                              self.operator_value,
                                                              self.shops_combo.currentText(),
                                                              self.passage_combo.currentText()), 'jpg'):
                self.save_status.setText(
                    'Ошибка сохранения! Обратитесь к администратору')
                self.save_status.setStyleSheet('background-color: red')
            self.i += 1
            self.count_label.setText(f'Нажатий: {self.i}')
        elif self.count_mode == 0:
            model.open_camera(self.cam_address_value)
            self.main_button.setText('Начать')
            self.count_mode = 1
        else:
            self.count_mode = 2
            self.main_button.setText('Считать')
            # запись о начале интервала подсчета
            model.set_time_interval(self.operator_value, self.shops_combo.currentText(
            ), self.passage_combo.currentText(), 'start')
            # активация таймера
            self.timer.start()
            # активация рекордера
            self.recorder_up = True
            t1 = threading.Thread(target=self.recorder)
            t1.start()

    def lock(self):
        if self.lock_flag:
            # активация кнопки счетчика
            self.main_button.setEnabled(True)
            # деактивация кнопок меню настроек
            self.shops_combo.setEnabled(False)
            self.operators_combo.setEnabled(False)
            self.passage_combo.setEnabled(False)
            self.lock_flag = False
            self.work_dir = model.make_directory(self.operator_value,
                                                 self.shops_combo.currentText(),
                                                 self.passage_combo.currentText())
            self.time_difference = model.find_time_difference(
                self.shops_combo.currentText())
            cam_connection = model.get_cam_connection(
                self.shops_combo.currentText(), self.passage_combo.currentText())
            if cam_connection:
                self.cam_address_value = cam_connection[0]
                self.login_value = cam_connection[1]
                self.password_value = cam_connection[2]
            else:
                self.cam_address_value = 'Нет камеры!'
                self.login_value = 'Нет камеры!'
                self.password_value = 'Нет камеры!'
            self.login_label.setText(f'Логин: {self.login_value}')
            self.password_label.setText(f'Пароль: {self.password_value}')
            self.cam_address_label.setText(f'Камера: {self.cam_address_value}')
            self.time_label.setText(
                f'Разница во времени с Москвой: +{self.time_difference}')
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
            # запись о завершении интервала подсчета
            model.set_time_interval(self.operator_value, self.shops_combo.currentText(
            ), self.passage_combo.currentText(), 'end')
            # остановка и сброс таймера
            self.timer.stop()
            self.time = 0
            self.timer_label.setStyleSheet('')
            # остановка рекордера
            self.recorder_up = False

    def copy_login(self):
        self.clipboard.setText(self.login_value)

    def copy_password(self):
        self.clipboard.setText(self.password_value)

    def set_operator(self):
        if self.operator_input_password.text() == '1488':
            self.operator_value = self.operators_combo.currentText()
            if model.set_operator(self.operator_value):
                self.operators_label.setText(
                    f'Оператор: {self.operator_value}')
                self.operator_input_password.clear()
            else:
                print('Ошибка добавления оператора')

    def cam_problem_report(self):
        if model.cam_problem_report(self.operator_value, self.shops_combo.currentText(
        ), self.cam_address_value, self.problem_description.text()):
            self.problem_description.clear()
        else:
            self.problem_description.setPlaceholderText(
                'Ошибка отправки')

    def updateUptime(self):
        self.time += 1
        self.settimer(self.time)

    def settimer(self, int):
        self.time = int
        if self.time > 3600:
            self.timer_label.setStyleSheet('background-color: green')

        self.timer_label.setText(time.strftime(
            'Часы: %H  Минуты: %M Секунды: %S', time.gmtime(self.time)))

    def recorder(self):

        resolution = tuple(pyautogui.size())
        fps = 12.0
        codec = cv2.VideoWriter_fourcc(*"MJPG")
        filename = model.make_record_name(
            self.work_dir, self.shops_combo.currentText())
        writer = cv2.VideoWriter(str(filename), codec, fps, resolution)

        while True:
            img = pyautogui.screenshot()
            # Convert the screenshot to a numpy array
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR to RGB
            # Writing it to the output file
            writer.write(frame)
            if self.recorder_up == False:
                break
        print("Recordings saved as: "+filename)
        writer.release()
        cv2.destroyAllWindows()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
