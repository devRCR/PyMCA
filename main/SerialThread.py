import serial, sys
from PyQt5.QtCore import pyqtSignal, QThread, QObject

class SerialPort(QThread):
    msg_byte=pyqtSignal(bytes)
    msg_str =pyqtSignal(str)

    def __init__(self, parent=None):
        super(SerialPort,self).__init__(parent)
        self.baud = 115200
        self.timeout = None
        self.isopen = False
        self.seriport=serial.Serial()

    def __del__(self):
        self.seriport.close()
        self.wait()

    def IsOpen(self):
        return self.isopen

    def Open(self, portname, baudrate):
        self.seriport.port = portname
        self.seriport.baudrate = baudrate
        try:
            self.seriport.open()
            self.isopen = True
        except (OSError, serial.SerialException):
            pass

    def OpenList(self, portname):
        if self.isopen == False:
            self.seriport.port = portname
            try:
                self.seriport.open()
                self.isopen = True
            except (OSError, serial.SerialException):
                pass

    def Close(self):
        if self.isopen:
            try:
                self.seriport.close()
                self.isopen=False
            except:
                pass

    def Send(self,message):
        newmessage = message.strip()
        #newmessage += '\r\n'
        self.seriport.write(newmessage.encode('utf-8'))

    def run(self):
        while True:
            try:
                if self.isopen:
                    stringData = self.seriport.read_until(b'\x00').decode('utf-8').replace('\x00', '').strip()
                    self.msg_str.emit(stringData) # pipeline
                    #print(stringData)
            except:
                pass
