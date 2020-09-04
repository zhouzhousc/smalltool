#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/15

import starpusher
import threading
from serial import Serial
import serial.tools.list_ports
import time
import sys
import os

# # 生成资源文件目录访问路径
# def resource_path(relative_path):
#     if getattr(sys, 'frozen', False):  # 是否Bundle Resource
#         base_path = sys._MEIPASS
#     else:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)
#
#
# # 访问res文件夹下a.txt的内容
# filename = resource_path(os.path.join("res", "a.txt"))
# print(filename)
# with open(filename) as f:
#     lines = f.readlines()
#     print(lines)
#     f.close()

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QGridLayout, QListWidget, QInputDialog, QLineEdit, QMessageBox, QDialog, QFileDialog, QTableWidgetItem, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime


class BackendThread(QThread):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currTime))
            time.sleep(1)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stop_flag = ""
        self.num_str = ""
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("炒鸡小工具")
        self.resize(580, 400)
        self.add_menu_and_statu()
        self.grid_layout()
        # self.listWidget()
        self.qthread(self.timedis)

    def qthread(self, handle):
        # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(handle)
        # 开始线程
        self.backend.start()

    # 添加菜单栏和状态栏
    def add_menu_and_statu(self):
        self.statusBar().showMessage("版本V0.0")
        # 创建一个菜单栏
        menu = self.menuBar()
        # 创建两个菜单
        file_menu = menu.addMenu("文件")
        file_menu.addSeparator()
        edit_menu = menu.addMenu('PG')
        edit_menu.addSeparator()

        # 创建一个行为
        new_action = QAction('打开文件', self)
        # 更新状态栏文本
        new_action.setStatusTip('数据文件')
        new_action.triggered.connect(self.openfile)
        # 设置退出打开键
        new_action.setShortcut('Ctrl+O')
        # 添加一个行为到菜单
        file_menu.addAction(new_action)

        # 创建退出行为
        exit_action = QAction('退出', self)
        # 退出操作
        exit_action.setStatusTip("点击退出应用程序")
        # 点击关闭程序
        exit_action.triggered.connect(self.close)
        # 设置退出快捷键
        exit_action.setShortcut('Ctrl+Q')
        # 添加退出行为到菜单上
        file_menu.addAction(exit_action)

        # 创建退出行为
        push_action = QAction('推箱子', self)
        # 退出操作
        push_action.setStatusTip("推箱子小游戏")
        # 点击关闭程序
        push_action.triggered.connect(self.thread_pushman)
        # 设置退出快捷键
        push_action.setShortcut('Ctrl+G')
        # 添加退出行为到菜单上
        edit_menu.addAction(push_action)

    # 网格布局
    def grid_layout(self):
        # 两个标签
        label_1 = QLabel('mpu数据串口采集')
        label_2 = QLabel('当前时间显示')
        self.label_i = QLabel('采集中')
        self.label_i.setVisible(False)
        self.label_f = QLabel('采集结束')
        self.label_f.setVisible(False)
        self.label_s = QLabel("")
        self.label_s.setVisible(False)
        self.label3 = QLabel(self)
        self.label3.setFixedWidth(113)
        self.label_4 = QLabel('采集数据耗时')
        self.label5 = QLabel(self)

        # 两个按钮
        button_1 = QPushButton('开始采集')
        button_2 = QPushButton('停止采集')
        button_3 = QPushButton('文件数据分析')
        button_4 = QPushButton('选定COM')
        button_5 = QPushButton('保存文件')
        button_6 = QPushButton('采集设定')
        button_1.clicked.connect(self.getText)
        button_2.clicked.connect(self.getInteger)
        button_3.clicked.connect(self.getDouble)
        button_4.clicked.connect(self.getChoice)
        button_5.clicked.connect(self.savefile)
        button_5.setShortcut('Ctrl+D')
        button_6.clicked.connect(self.getInteger2)

        # 创建一个网格布局对象
        grid_layout = QGridLayout()

        # 在网格中添加窗口部件
        grid_layout.addWidget(label_1, 0, 0)  # 放置在0行0列
        grid_layout.addWidget(button_1, 0, 2)  # 0行2列
        grid_layout.addWidget(label_2, 1, 0)  # 1行0列
        grid_layout.addWidget(button_2, 0, 3)  # 0行3列
        grid_layout.addWidget(button_3, 3, 0, 1, 1)
        grid_layout.addWidget(button_4, 0, 1)
        grid_layout.addWidget(button_5, 3, 1, 1, 1)
        grid_layout.addWidget(button_6, 3, 2, 1, 1)
        grid_layout.addWidget(self.label3, 1, 1)
        grid_layout.addWidget(self.label_4, 2, 0)
        grid_layout.addWidget(self.label5, 2, 1)
        grid_layout.addWidget(self.label_i, 1, 2)  # 1行2列
        grid_layout.addWidget(self.label_f, 1, 3)  # 1行3列
        grid_layout.addWidget(self.label_s, 3, 3)  # 3行3列

        self.textBrowser = QTextEdit()  # 创建文本框用于显示
        grid_layout.addWidget(self.textBrowser, 4, 0, 10, 4)

        # 对齐方式
        grid_layout.setAlignment(Qt.AlignTop)
        # grid_layout.setAlignment(label_1, Qt.AlignRight)

        # 创建一个窗口对象
        layout_widget = QWidget()
        # 设置窗口的布局层
        layout_widget.setLayout(grid_layout)

        self.setCentralWidget(layout_widget)

    def listWidget(self):
        self.listView = QListWidget(self)  # 实例化QListWidget
        self.listView.setGeometry(20, 120, 200, 100)  # 设置QListWidget在窗口中的位置与大小
        self.listView.addItem('点击关闭！！')  # 往QListWidget添加内容
        self.listView.addItem('点击也是关闭！！')  # 往QListWidget添加内容
        self.listView.itemClicked.connect(self.close)  # 给 QListWidget 每个项目设置点击事件

    def getText(self):
        self.text, okPressed = QInputDialog.getText(self, '保存文件', '请输入文件名', QLineEdit.Normal, "move.txt")

        if okPressed and self.text != '':
            self.label_f.setVisible(False)
            self.label_i.setVisible(True)
            print(self.text)
            self.thread_ser_data()

    def getIfom(self):
        reply = QMessageBox.information(self, '失败', '没有可用串口', QMessageBox.Retry | QMessageBox.Cancel)
        if reply == QMessageBox.Retry:
            self.getText()

    def getInteger(self):
        self.t2 = time.time()
        self.label5.setText(str(round(self.t2 - self.t1, 2)) + "s")
        self.stop_flag = "break_flag"
        self.label_i.setVisible(False)
        self.label_f.setVisible(True)
        self.label_s.setVisible(False)

        print("停止采集")

    def getInteger2(self):
        i, okPressed = QInputDialog.getInt(self, "采集数目", "数目设定:", 1600, 200, 5200, 200)
        if okPressed and i != 0:
            self.num_str = str(i)
            self.label_s.setText(self.num_str)
            self.label_s.setVisible(True)
            print(str(i))

    def getDouble(self):
        # d, okPressed = QInputDialog.getDouble(self, "浮点数", "选择浮点数:", 10.05, 0, 100, 3)
        # if okPressed:
        #     print(d)
        pass

    def getChoice(self):
        # Get item/choice
        items = []
        plist = list(serial.tools.list_ports.comports())
        for i in range(len(plist)):
            items.append(list(plist[i])[0])
        self.item, okPressed = QInputDialog.getItem(self, "选择com口", "COM：", items, 0, False)

        if okPressed and self.item:
            print(self.item)

    def thread_ser_data(self):
        t = threading.Thread(target=self.ser_data, name='ser_data')
        t.start()

    def thread_pushman(self):
        t2 = threading.Thread(target=starpusher.pushman, name='starpusher')
        t2.start()

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '*.txt')
        print(openfile_name)
        # global path_openfile_name
        if openfile_name[0][-4:] == '.txt':
            f = open(openfile_name[0], 'r', encoding="utf-8")
            my_data = f.read()
            f.close()
            self.textBrowser.setPlainText(my_data)

        # else:
        #     QMessageBox.information(self, 'Information', '不支持的文件格式')

    def savefile(self):
        filename = QFileDialog.getSaveFileName(self, 'save file')
        with open(filename[0], 'w') as f:
            my_text = self.textBrowser.toPlainText()
            f.write(my_text)

    def ser_data(self):
        self.t1 = time.time()
        self.count = 0
        self.stop_flag = "ok"
        try:
            sit = self.item

        except:
            plist = list(serial.tools.list_ports.comports())
            sit = list(plist[-1])[0]

        ser = Serial(port=sit, baudrate=115200)
        with open(self.text, 'w', encoding='utf-8', newline='') as f:  # 追加是a+
            f.write("ax,ay,az,gx,gy,gz,mx, my,mz,Yaw,Pitch,Roll,rate,count\n")

            while self.count < (int(self.num_str) + 1):
                if self.stop_flag == "break_flag":
                    break

                else:
                    try:
                        data = str(ser.readline(), encoding="utf-8")
                        print(data)
                        f.write(data)
                        self.count += 1

                    except Exception as e:
                        print(e)
                        time.sleep(1)
        # while self.count < 50000001:
        #     if self.stop_flag == "break_flag":
        #         break
        #     else:
        #
        #         self.count += 1
        #         print(self.count)
        ser.close()
        self.label_i.setVisible(False)
        self.label_f.setVisible(True)
        print("finished")

    def timedis(self, data):
        self.label3.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
