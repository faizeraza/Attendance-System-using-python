import cv2
import numpy as np
import face_recognition
import os
import pyttsx3
from datetime import datetime
import time
from PyQt5 import QtCore, QtGui, QtWidgets

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames[0])

class recognizer:
    def __init__(self,images,classNmaes,name):
        self.images = images
        self.classNames = classNmaes
        self.name = name
        self.engine = pyttsx3.init()
    def findEncodings(self):
        encodeList = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(self):
        with open('presenty.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if self.name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{self.name},{dtString}')
                self.engine.say(f"Thank you {self.name} your attendance is marked successfully")
                self.engine.runAndWait()
#*************************end-recognizer*********************************
naam = "Name"
recogniz = recognizer(images,classNames,naam)
encodeListKnown = recogniz.findEncodings()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(371, 501)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 371, 361))
        self.graphicsView.setObjectName("graphicsView")

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

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            #img = captureScreen()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis)
            
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    #print(name)
                    y1,x2,y2,x1 = faceLoc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    recogniz2 = recognizer(images,classNames,name)
                    recogniz2.markAttendance()
                        
                    cv2.imshow('Webcam',img)
                    cv2.waitKey(1)

            
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