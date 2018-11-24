#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import PyQt5.QtWidgets as wgt
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QIntValidator
import serial

import cv2

class SerialCombobox(wgt.QComboBox):
    def __init__(self):
        super().__init__()

        import serial.tools.list_ports
        comports = list(serial.tools.list_ports.comports()[0])
        valid_comports = [port for port in comports if port.startswith('/dev')]

        self.addItems(valid_comports)


class ServoSlider(wgt.QWidget):

    def __init__(self, type, idx):
        super().__init__()

        self.sld        = wgt.QSlider(type, self)
        self.sld_lbl    = wgt.QLabel(self)

        if type == Qt.Horizontal:
            layout = wgt.QHBoxLayout(self)
        else:
            layout = wgt.QVBoxLayout(self)

        self.setLayout(layout)
        layout.addWidget(self.sld)
        layout.addWidget(self.sld_lbl)

        self.sld.setTickPosition(wgt.QSlider.TicksBelow)

        self.idx = idx

        self.setLimits(0, 1000)

        self.sld.valueChanged[int].connect(self.changeValue)

        self.serial = None

    def setLimits(self, min_value, max_value):

        self.sld.setMinimum(min_value)
        self.sld.setMaximum(max_value)

    def getLimits(self):
        return (self.sld.minimum(), self.sld.maximum())

    def getIndex(self):
        return self.idx

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


class CameraWidget(wgt.QLabel):

    def __init__(self, width=640, height=480):
        super().__init__()

        self.setSource(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.setMinimumWidth(width)
        self.setMinimumHeight(height)

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


class SetupSliderLimit(wgt.QWidget):

    def __init__(self, slider):
        # slider: [ServoSlider]

        super().__init__()

        self.sliderWgt = slider
        self.minValue, self.maxValue = self.sliderWgt.getLimits()

        layout = wgt.QHBoxLayout(self)
        self.setLayout(layout)

        labelMax = wgt.QLabel('Max:', self)
        labelMin = wgt.QLabel('Min:', self)
        labelIdx = wgt.QLabel('Servo {}'.format(str(self.sliderWgt.getIndex())), self)

        self.textMax = wgt.QLineEdit(str(self.maxValue), self)
        self.textMax.setValidator( QIntValidator(0, 99999) )
        self.textMax.editingFinished.connect(self.slotTextMaxChanged)

        self.textMin = wgt.QLineEdit(str(self.minValue), self)
        self.textMin.setValidator( QIntValidator(0, 99999) )
        self.textMin.editingFinished.connect(self.slotTextMinChanged)

        layout.addWidget(labelIdx)
        layout.addWidget(labelMin)
        layout.addWidget(self.textMin)
        layout.addWidget(labelMax)
        layout.addWidget(self.textMax)

    def slotTextMaxChanged(self):
        try:
            input = int(self.textMax.text())
            self.maxValue = input
        except:
            print('Invalid input')

    def slotTextMinChanged(self):
        try:
            input = int(self.textMin.text())
            self.minValue = input
        except:
            print('Invalid input')

    def applyLimits(self):
        # Call it again to update values
        self.slotTextMinChanged()
        self.slotTextMaxChanged()

        # Swap
        if self.minValue > self.maxValue:
            tmp             = self.minValue
            self.minValue   = self.maxValue
            self.maxValue   = tmp

        self.sliderWgt.setLimits( self.minValue, self.maxValue )


class SetupMenu(wgt.QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Setup')

        # baseWgt = wgt.QWidget(self)
        baseLayout = wgt.QVBoxLayout()
        # self.setCentralWidget(baseWgt)
        self.setLayout(baseLayout)

        # Buttons init 

        btnsWgt = wgt.QWidget(self)
        btnsLayout = wgt.QHBoxLayout()
        btnsWgt.setLayout(btnsLayout)

        applyBtn = wgt.QPushButton('Apply', self)
        applyBtn.clicked[bool].connect(self.applyPressed)

        cancelBtn = wgt.QPushButton('Cancel', self)
        cancelBtn.clicked[bool].connect(lambda bool: self.reject())

        btnsLayout.addWidget(applyBtn)
        btnsLayout.addWidget(cancelBtn)

        # Main window init

        setupWgt = wgt.QWidget(self)
        self.setupLayout = wgt.QGridLayout()
        setupWgt.setLayout(self.setupLayout)

        # Set widgets order

        baseLayout.addWidget(setupWgt)
        baseLayout.addWidget(btnsWgt)

        # Internal logic
        self.sliderSetups = []

    def addSlider(self, slider):
        # slider: [ServoSlider]
        
        sliderSetup = SetupSliderLimit(slider)

        self.setupLayout.addWidget(sliderSetup, len(self.sliderSetups), 0)

        self.sliderSetups.append(sliderSetup)

    def applyPressed(self, bool):
        for sliderSetup in self.sliderSetups:
            sliderSetup.applyLimits()

        self.accept()

class MainWindow(wgt.QMainWindow):

    def __init__(self):
        super().__init__()

        # Common init

        self.setWindowTitle('ServoControl')
        
        centralWidget = wgt.QWidget(self)
        self.setCentralWidget(centralWidget)

        layout = wgt.QGridLayout()
        centralWidget.setLayout(layout)
        layout.setSpacing(10)

        # Camera widget

        self.cameraWidget = CameraWidget()
        layout.addWidget(self.cameraWidget, 0, 0)

        # Slider widgets

        self.servoSlider1 = ServoSlider(Qt.Horizontal, 1)
        self.servoSlider2 = ServoSlider(Qt.Vertical, 2)
        layout.addWidget(self.servoSlider1, 1, 0)
        layout.addWidget(self.servoSlider2, 0, 1)

        # Defaults
        self.servoSlider1.setLimits(1000, 2000)
        self.servoSlider2.setLimits(1000, 2000)

        # Control widget 

        self.controlWidget = wgt.QWidget(self)
        controlLayout = wgt.QGridLayout()
        self.controlWidget.setLayout( controlLayout )

        layout.addWidget(self.controlWidget, 2, 0, 1, 2)

        # Camera control

        self.captureBtn = wgt.QPushButton('Start Camera', self)
        self.captureBtn.setCheckable(True)
        self.captureBtn.clicked[bool].connect(self.toggleCameraState)
        controlLayout.addWidget(self.captureBtn, 0, 0, 1, 2)

        # Serial control

        self.serialBtn = wgt.QPushButton('Start Serial', self)
        self.serialBtn.setCheckable(True)
        self.serialBtn.clicked[bool].connect(self.toggleSerialState)
        controlLayout.addWidget(self.serialBtn, 1, 0)

        self.serialCmbBox = SerialCombobox()
        controlLayout.addWidget(self.serialCmbBox, 1, 1)

        # Setup window

        self.setupMenu = SetupMenu()
        self.setupMenu.addSlider(self.servoSlider1)
        self.setupMenu.addSlider(self.servoSlider2)

        # Menu init

        setupAction = wgt.QAction('&Setup', self)
        setupAction.setShortcut('Ctrl+W')
        setupAction.setStatusTip('Open setup')
        setupAction.triggered.connect(self.showSetupWindow)

        menubar = self.menuBar()
        setupMenu = menubar.addMenu('&Menu')
        setupMenu.addAction(setupAction)


    def showSetupWindow(self):
        self.setupMenu.show()

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

    app = wgt.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())