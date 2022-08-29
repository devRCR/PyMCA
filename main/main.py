#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, time
import numpy as np
import threading
from SerialThread import *
from gui import *
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings, QPoint
import inspect

class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		self.my_index = []
		self.adc_channel = np.zeros(4096)

		self.getData = False

		self.mySerial = SerialPort()
		self.ListPorts()

		self.pushButton_Start.clicked.connect(self.StartProcess)
		self.pushButton_Stop.clicked.connect(self.StopProcess)
		self.pushButton_UpdatePorts.clicked.connect(self.ListPorts)
		self.pushButton_OpenClosePort.clicked.connect(self.OpenClosePort)

		self.mySerial.msg_str.connect(self.plainTextData.appendPlainText)
		self.mySerial.msg_str.connect(self.GetData)


	def ListPorts(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(100)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			ports = ['/dev/ttyACM%s' % i for i in range(100)]
			for i in range(100):
				ports.append('/dev/ttyUSB%s' % i)
		else:
			raise EnvironmentError('Unsupported platform')
		result = []
		for port in ports:
			self.mySerial.OpenList(port)
			if self.mySerial.IsOpen() == True:
				result.append(port)
			self.mySerial.Close()
		self.comboBox_ComPort.clear()
		self.comboBox_ComPort.addItems(result)

	def OpenClosePort(self):
		if self.pushButton_OpenClosePort.text() == 'Open Port':
			comport = self.comboBox_ComPort.currentText()
			baudrate = self.comboBox_BaudRate.currentText()
			self.mySerial.Open(comport,baudrate)
			if self.mySerial.IsOpen():
				self.mySerial.start()
				self.pushButton_OpenClosePort.setText('Close Port')
				self.pushButton_Start.setEnabled(True)
		elif self.pushButton_OpenClosePort.text() == "Close Port":
			self.mySerial.Close()
			if self.mySerial.IsOpen() == False:
				self.pushButton_OpenClosePort.setText('Open Port')
				self.pushButton_Start.setEnabled(False)

	def StartProcess(self):
		self.plotWidget.canvas.ax.clear()
		self.Plot()
		self.PlotData()

		if self.mySerial.IsOpen():
			self.mySerial.Send('START:')
			self.pushButton_Stop.setEnabled(True)
			self.pushButton_Start.setEnabled(False)
			self.pushButton_OpenClosePort.setEnabled(False)

	def StopProcess(self):
		if self.mySerial.IsOpen():
			self.mySerial.Send('STOP:')
			self.pushButton_Stop.setEnabled(False)
			self.pushButton_Start.setEnabled(True)
			self.pushButton_OpenClosePort.setEnabled(True)

	def GetData(self,stringData):
		if len(stringData) != 0:
			self.adc_channel[int(stringData)-1] += 1
		
	def PlotData(self):
		threading.Timer(1.0, self.PlotData).start()
		self.plotWidget.canvas.ax.plot(self.adc_channel,color='blue', marker='o', markersize = 0.5, linestyle='none')


	def Plot(self):
		#self.plotWidget.canvas.ax.grid(True)
		self.plotWidget.canvas.ax.set_ylabel('Energy (kV)')
		self.plotWidget.canvas.ax.set_xlabel('Channel')
		self.plotWidget.canvas.ax.set_title('Spectrometer')
		self.plotWidget.canvas.draw()    

if __name__=='__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
