import os
from random import choice

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from support import *
from ui_file import Ui_MainWindow

CITY = open('country.txt', "r", encoding="utf-8").read().split(', ')  # 1116 городов


def save_image(city):
    toponym_to_find = city
    toponym = get_response(toponym_to_find)
    spn_toponym = ','.join(map(lambda x: str(float(x) / 10),
                               get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                                       toponym['boundedBy']['Envelope']['upperCorner']).split(',')))
    ll_toponym = ','.join(map(lambda x: str(float(x)), toponym['Point']['pos'].split()))

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(get_response_map(ll_toponym, spn_toponym))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.player = -1
        self.points = [0, 0]
        self.city_draw = choice(CITY)
        self.answer_btn.clicked.connect(self.check_answer)
        self.set_setting()

    def check_answer(self):
        if self.answer_line_edit.text().lower() == self.city_draw.lower():
            self.points[self.player] += 1
            self.set_setting()
        else:
            if self.player == 1:
                city = self.city_draw
                self.set_setting()
                self.no_answer.setText(f'Это был(а): {city}')
            else:
                self.player += 1
                self.label_2.setText(f"Игрок номер {self.player + 1} ваш ответ: ")

    def set_setting(self):
        self.points_1.setText(f'Игрок номер 1: {str(self.points[0])} очка(ов)')
        self.points_2.setText(f'Игрок номер 2: {str(self.points[1])} очка(ов)')
        self.player = 0
        self.city_draw = choice(CITY)
        save_image(self.city_draw)
        self.label_2.setText(f"Игрок номер {self.player + 1} ваш ответ: ")
        self.label_map.setPixmap(QPixmap('map.png'))
        os.remove('map.png')
        self.no_answer.setText('')
        # print(self.city_draw)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
