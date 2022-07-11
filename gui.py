# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attendancegui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import time
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(371, 501)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.QRect(0, 0, 371, 361))
        # self.graphicsView.setObjectName("graphicsView")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 360, 371, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("offdone.jpg"))
        self.label.setObjectName("label")

        self.donebtn = QtWidgets.QPushButton(self.centralwidget)
        self.donebtn.setEnabled(True)
        self.donebtn.setGeometry(QtCore.QRect(140, 450, 71, 31))
        self.donebtn.setText("")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("offdone.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("done.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.donebtn.setIcon(icon)
        self.donebtn.setCheckable(True)
        self.donebtn.setChecked(False)
        self.donebtn.setAutoDefault(False)
        self.donebtn.setObjectName("donebtn")
        self.donebtn.clicked.connect(self.doAction)
        
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(100, 390, 171, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def doAction(self):
  
        # setting for loop to set value of progress bar
        for i in range(101):
  
            # slowing down the loop
            time.sleep(0.05)
  
            # setting value to progress bar
            self.progressBar.setValue(i)
            
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
