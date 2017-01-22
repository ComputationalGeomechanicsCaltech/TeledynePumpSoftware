# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotter.ui'
#
# Created: Wed Jan 18 17:04:34 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TeledynePlotter(object):
    def setupUi(self, TeledynePlotter):
        TeledynePlotter.setObjectName(_fromUtf8("TeledynePlotter"))
        TeledynePlotter.resize(1126, 895)
        self.centralwidget = QtGui.QWidget(TeledynePlotter)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pressure_graph = PlotWidget(self.centralwidget)
        self.pressure_graph.setGeometry(QtCore.QRect(10, 70, 1091, 251))
        self.pressure_graph.setObjectName(_fromUtf8("pressure_graph"))
        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(630, 10, 101, 51))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.stopButton = QtGui.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(750, 10, 101, 51))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 20, 471, 41))
        self.plainTextEdit.setStyleSheet(_fromUtf8("font: 63 11pt \"Ubuntu\";"))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.newButton = QtGui.QPushButton(self.centralwidget)
        self.newButton.setGeometry(QtCore.QRect(510, 10, 101, 51))
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.StartPumpButton = QtGui.QPushButton(self.centralwidget)
        self.StartPumpButton.setGeometry(QtCore.QRect(870, 10, 101, 51))
        self.StartPumpButton.setObjectName(_fromUtf8("StartPumpButton"))
        self.StopPumpButton = QtGui.QPushButton(self.centralwidget)
        self.StopPumpButton.setGeometry(QtCore.QRect(990, 10, 101, 51))
        self.StopPumpButton.setObjectName(_fromUtf8("StopPumpButton"))
        self.force_graph = PlotWidget(self.centralwidget)
        self.force_graph.setGeometry(QtCore.QRect(10, 330, 1091, 251))
        self.force_graph.setObjectName(_fromUtf8("force_graph"))
        self.displacement_graph = PlotWidget(self.centralwidget)
        self.displacement_graph.setGeometry(QtCore.QRect(10, 590, 1091, 251))
        self.displacement_graph.setObjectName(_fromUtf8("displacement_graph"))
        TeledynePlotter.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TeledynePlotter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        TeledynePlotter.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TeledynePlotter)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        TeledynePlotter.setStatusBar(self.statusbar)

        self.retranslateUi(TeledynePlotter)
        QtCore.QMetaObject.connectSlotsByName(TeledynePlotter)

    def retranslateUi(self, TeledynePlotter):
        TeledynePlotter.setWindowTitle(_translate("TeledynePlotter", "MainWindow", None))
        self.startButton.setText(_translate("TeledynePlotter", "Start Test", None))
        self.stopButton.setText(_translate("TeledynePlotter", "Stop Test", None))
        self.newButton.setText(_translate("TeledynePlotter", "New Test", None))
        self.StartPumpButton.setText(_translate("TeledynePlotter", "Start Pump", None))
        self.StopPumpButton.setText(_translate("TeledynePlotter", "Stop Pump", None))

from pyqtgraph import PlotWidget
