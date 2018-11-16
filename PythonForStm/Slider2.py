#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QSlider,
    QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import serial

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
flag1=0
flag2=0
flag3=0
flag4=0

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('mute.png'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()


    def changeValue(self, value):
        
        global flag1
        global flag2
        global flag3
        global flag4
        if value == 0:
            self.label.setPixmap(QPixmap('mute.png'))
            if flag1==0:
                flag1=1
                flag2=0
                flag3=0
                flag4=0
                x = 1
                data = bytes([int(x)])
                ser.write(data)
                print(x)
            
        elif value > 0 and value <= 30:
            if flag2==0:
                flag1=0
                flag2=1
                flag3=0
                flag4=0
                x = 2
                data = bytes([int(x)])
                ser.write(data)
                print(x)
            
        elif value > 30 and value < 80:
            if flag3==0:
                flag1=0
                flag2=0
                flag3=1
                flag4=0
                x = 3
                data = bytes([int(x)])
                ser.write(data)
                print(x)
            
        else:
            if flag4==0:
                flag1=0
                flag2=0
                flag3=0
                flag4=1
                x = 4
                data = bytes([int(x)])
                ser.write(data)
                print(x)
            


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())