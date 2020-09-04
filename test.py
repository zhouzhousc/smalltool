#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/6/2

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QCheckBox
import sys


class ui(QWidget):
    def __init__(self):
        super().__init__()
        self.show_ui()

    def show_ui(self, y=50):
        self.pu = QPushButton(self)
        self.pu.setText('隐藏按键')
        self.pu.setVisible(False)
        self.pu.setGeometry(50, y, 100, 50)
        self.bt = QPushButton(self)
        self.bt.setText("可见按键")
        self.bt.setGeometry(150, y, 100, 50)
        self.bt.clicked.connect(self.keyPressEvent)
        self.cb = QCheckBox(self)
        self.cb.setText("隐藏的复选框")
        self.cb.setVisible(False)
        self.setGeometry(500, 500, 580, 370)
        self.setWindowTitle('check my button')

    def keyPressEvent(self, QKeyEvent):  # 键盘触发
        self.show_ui(70)
        self.pu.setVisible(True)  # 只有设置为True 才能显示  之前默认都是显示的  但是在这添加就默认不显示了
        self.cb.setVisible(True)  # 复选框也可以设置隐藏和显示
        print('sde')  # 验证事件是否触发


if __name__ == '__main__':
    app = QApplication(sys.argv)
    u = ui()
    u.show()
    sys.exit(app.exec_())
