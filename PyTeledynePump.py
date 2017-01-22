from PyQt4 import QtGui,QtCore
import sys, serial, io
import plotter
import numpy as np
import pylab
import time
from time import sleep
import pyqtgraph
from datetime import datetime
from Tkinter import Tk
from tkFileDialog import asksaveasfile
from tkMessageBox import showerror
#from Tkinter.filedialog import asksaveasfile
#from Tkinter.messagebox import showerror
from random import randint
from collections import deque

class ExampleApp(QtGui.QMainWindow, plotter.Ui_TeledynePlotter):
    
    def __init__(self, parent=None):
    
        self.port = "/dev/ttyACM0"
        self.baudrate = 19200
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS
        self.timeout = 1
        self.ser = None
        
        #self.connect_to_pump()

        self.port2 = "/dev/ttyUSB0"
        self.baudrate2 = 115200
        self.parity2 = serial.PARITY_NONE
        self.stopbits2 = serial.STOPBITS_ONE
        self.bytesize2 = serial.EIGHTBITS
        self.timeout2 = 0.001
        self.ser2 = None
        
        self.connect_to_datalogger()
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.startButton.clicked.connect(self.start_test)
        self.stopButton.clicked.connect(self.stop_test)
        self.newButton.clicked.connect(self.new_test)
        self.StartPumpButton.clicked.connect(self.start_pump)
        self.StopPumpButton.clicked.connect(self.stop_pump)
        
        self.pressure_graph.plotItem.showGrid(True, True, 0.7)
        self.force_graph.plotItem.showGrid(True, True, 0.7)
        self.displacement_graph.plotItem.showGrid(True, True, 0.7)
        self.color = pyqtgraph.hsvColor(0.38,0.92,0.47,alpha=.5)
        self.pen = pyqtgraph.mkPen(color=self.color,width=10)
        self.num_points = 100
        self.X = np.arange(self.num_points)
        self.pressure = deque([0.0]*self.num_points)
        self.force = deque([0.0]*self.num_points)
        self.displacement = deque([0.0]*self.num_points)
        self.filename = None
        self.plainTextEdit.appendPlainText('No filename')
        
        self.test = False
        self.pump_running = False

    def connect_to_datalogger(self):
        print("Connect to datalogger, reading from serial port {} ...".format(self.port2))
        num_attempts = 5
        for i in range(1, num_attempts):
            if i is num_attempts-1:
                print('Failed too many times.  Exiting')
                exit()
            try:
                self.ser2 = serial.Serial(port = self.port2,
                                         baudrate = self.baudrate2,
                                         parity = self.parity2,
                                         stopbits = self.stopbits2,
                                         bytesize = self.bytesize2,
                                         timeout = self.timeout2)
                self.ser2.flush()
                print('Success.')
                break
            except ValueError:
                print("Attempt {}: Parameters out of range, e.g. baud rate, data bits. Retrying ...".format(i))
                sleep(2)
            except serial.SerialException:
                print("Attempt {}: Device can not be found or can not be configured. Retrying ...".format(i))
                sleep(2)

    def connect_to_pump(self):
        print("Connect to pump, reading from serial port {} ...".format(self.port))
        num_attempts = 5
        for i in range(1, num_attempts):
            if i is num_attempts-1:
                print('Failed too many times.  Exiting')
                exit()
            try:
                self.ser = serial.Serial(port = self.port,
                                         baudrate = self.baudrate,
                                         parity = self.parity,
                                         stopbits = self.stopbits,
                                         bytesize = self.bytesize,
                                         timeout = self.timeout)
                self.ser.flush()
                print('Success.')
                break
            except ValueError:
                print("Attempt {}: Parameters out of range, e.g. baud rate, data bits. Retrying ...".format(i))
                sleep(2)
            except serial.SerialException:
                print("Attempt {}: Device can not be found or can not be configured. Retrying ...".format(i))
                sleep(2)

    def file_header(self):
        header = 'Hour, Minute, Second, Pressure (psi), Force (??), Displacement (??)\n'
        return header

    def new_test(self):
        if self.test is True:
            showerror("New Test", "Test currently running!")
            return
        if self.filename is not None:
            self.filename.close()
            self.filename = None
            
        self.filename = asksaveasfile(mode='w',
                                      defaultextension=".txt")
        if self.filename is None:
            return
        
        self.filename.write(self.file_header())
        self.filename.flush()
        self.show_filename()

    def show_filename(self):
        if self.filename is None:
            self.plainTextEdit.appendPlainText('No filename')
            return
        self.plainTextEdit.appendPlainText(self.filename.name)

    def start_test(self):
        if self.filename is None:
            showerror("Start Test", "Need to select new test first!")
            return
        if self.test is True:
            showerror("Start Test", "A test is running!")
            return
        self.pressure = deque([0.0]*self.num_points)
        self.force = deque([0.0]*self.num_points)
        self.displacement = deque([0.0]*self.num_points)
        self.test = True
        self.update()

    def start_pump(self):
        if self.pump_running is False:
            self.ser.write("RU\r")
            self.pump_running = True
            dummy = self.read_pump_line()

    def stop_pump(self):
        if self.pump_running is True:
            self.ser.write("ST\r")
            self.pump_running = False
            dummy = self.read_pump_line()

    def stop_test(self):
        if self.test is False:
            showerror("Stop Test", "No test running")
            return
        self.test = False
        self.filename.close()
        self.filename = None
        self.show_filename()

    def get_pressure_data(self):
        self.ser.write("PR\r")
        line = self.read_pump_line()
        if line is '':
            self.filename.write('-9999')
            print('Possible read error:\n')
            print(line)
        else:
            self.filename.write(line[-5:-1])
        dummy = self.pressure.pop()
        try:
            self.pressure.appendleft(float(line[-5:-1]))
        except ValueError:
            self.pressure.appendleft(dummy)

    def read_pump_line(self):
        # return ead 
        eol = '/'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return str(line)

    def get_mechanical_data(self):

        line = self.read_data_logger_line()
        self.filename.write(line+'\n')
        self.filename.flush()
        data = line.split(',')
        force_dummy = self.force.pop()
        displacement_dummy = self.displacement.pop()
        try:
            self.force.appendleft(float(data[0]))
            self.displacement.appendleft(float(data[1]))
        except ValueError:
            self.force.appendleft(force_dummy)
            self.displacement.appendleft(displacement_dummy)
        
    def read_data_logger_line(self):

        while self.ser2.inWaiting() is not 0:
            self.ser2.flushInput()

        eol = '\n'
        leneol = len(eol)
        line = bytearray()
        first = True
        while True:
            c = self.ser2.read(1)
            if c:
                if c == eol and first is False:
                    break
                elif c == eol and first is True:
                    first = False
                    line = bytearray()
                else:
                    line += c
                
        return str(line)

    def update(self):
        if self.test is True:
            t1=datetime.now().strftime("%H, %M, %S.%f, ")
            self.filename.write(t1)
            #self.get_pressure_data()
            self.get_mechanical_data()
            self.pressure_graph.plot(self.X,self.pressure,pen=self.pen,clear=True)
            self.force_graph.plot(self.X,self.force,pen=self.pen,clear=True)
            self.displacement_graph.plot(self.X,self.displacement,pen=self.pen,clear=True)
            QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

    def close_connection(self):
        self.ser.close()

if __name__=="__main__":
    Tk().withdraw()
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    #app.close_connection()
    print("DONE")
    exit()
