#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QApplication, QGridLayout, QSizePolicy, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import serial

import cv2

class SerialCombobox(QComboBox):
    def __init__(self):
        super().__init__()

        import serial.tools.list_ports
        comports = list(serial.tools.list_ports.comports()[0])
        valid_comports = [port for port in comports if port.startswith('/dev')]

        self.addItems(valid_comports)


class ServoSlider(QWidget):

    def __init__(self, type, idx):
        super().__init__()

        self.sld        = QSlider(type, self)
        self.sld_lbl    = QLabel()

        if type == Qt.Horizontal:
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()

        self.setLayout(layout)
        layout.addWidget(self.sld)
        layout.addWidget(self.sld_lbl)

        self.sld.setTickPosition(QSlider.TicksBelow)

        self.idx = idx

        self.setLimits(0, 1000)

        self.sld.valueChanged[int].connect(self.changeValue)

        self.serial = None

    def setLimits(self, min_value, max_value):

        self.sld.setMinimum(min_value)
        self.sld.setMaximum(max_value)

    def getLimits(self):
        return (self.sld.minimum(), self.sld.maximum())

    def enableCommunication(self, serial):
        self.serial = serial

    def disableCommunication(self):
        self.serial = None

    def changeValue(self, value):

        self.sld_lbl.setText(str(value))

        if self.serial:
            x = value
            self.serial.write(bytes([ord('#'), self.idx]))
            y = value.to_bytes(2, byteorder='big') #convert to byte array
            self.serial.write(y)


class CameraWidget(QLabel):

    def __init__(self, width=640, height=480):
        super().__init__()

        self.setSource(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.setFixedWidth(width)
        self.setFixedHeight(height)

    def update_frame(self):
        
        retval, img = self.cap.read()

        img = cv2.resize(img, (self.width(), self.height()))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        height, width, bpc = img.shape
        bpl = bpc * width
        image = QImage(img.data, width, height, bpl, QImage.Format_RGB888)
        
        pixmap = QPixmap(image)
        self.setPixmap(pixmap)


    def setSource(self, source):
        self.cap = cv2.VideoCapture(source)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width())
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height())

    def startCapture(self):
        self.timer.start(.01)

    def stopCapture(self):
        self.timer.stop()

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('ServoControl')        
        
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(10)

        self.cameraWidget = CameraWidget()
        layout.addWidget(self.cameraWidget, 0, 0)

        self.servoSlider1 = ServoSlider(Qt.Horizontal, 1)
        self.servoSlider2 = ServoSlider(Qt.Vertical, 2)
        layout.addWidget(self.servoSlider1, 1, 0)
        layout.addWidget(self.servoSlider2, 0, 1)

        self.controlWidget = QWidget(self)
        controlLayout = QGridLayout()
        self.controlWidget.setLayout( controlLayout )

        layout.addWidget(self.controlWidget, 2, 0, 1, 2)

        self.captureBtn = QPushButton('Start Camera', self)
        self.captureBtn.setCheckable(True)
        self.captureBtn.clicked[bool].connect(self.toggleCameraState)
        controlLayout.addWidget(self.captureBtn, 0, 0, 1, 2)

        self.serialBtn = QPushButton('Start Serial', self)
        self.serialBtn.setCheckable(True)
        self.serialBtn.clicked[bool].connect(self.toggleSerialState)
        controlLayout.addWidget(self.serialBtn, 1, 0)

        self.serialCmbBox = SerialCombobox()
        controlLayout.addWidget(self.serialCmbBox, 1, 1)


    def toggleSerialState(self, state):
        if state:
            self.serialBtn.setText('Stop Serial')

            self.ser = serial.Serial(self.serialCmbBox.currentText(), 115200,timeout=1)
            self.servoSlider1.enableCommunication(self.ser)
            self.servoSlider2.enableCommunication(self.ser)

        else:
            self.serialBtn.setText('Start Serial')

            self.servoSlider1.disableCommunication()
            self.servoSlider2.disableCommunication()
            self.ser.close()


    def toggleCameraState(self, state):
        if state:
            self.captureBtn.setText('Stop Camera')

            self.cameraWidget.startCapture()
        else:
            self.captureBtn.setText('Start Camera')

            self.cameraWidget.stopCapture()

    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())