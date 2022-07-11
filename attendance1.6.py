import cv2
import numpy as np
import face_recognition
import os
import pyttsx3
from datetime import datetime
import time
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QFont
import sys
import subprocess
import pandas as pd


data = pd.read_csv("database/record.csv")
data.set_index("Name", inplace=True)
#listing down the images present in folder
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

#reading and storing image in list (images) and image name in (classNames)
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

    #Image encoding is used on dataset features that are image files, like jpg and png files.
    #Given an image,return list containing array of the 128-dimension face encoding for each face in the image.
    def findEncodings(self):
        encodeList = []
        for img in self.images:
            #converting img from BGR color space to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    #below function will take name current face present on cam and check wheather it is present
    # in the csv if not then add on list. 
    def markAttendance(self):
        with open('database/presenty.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            #add names present in csv line by line if any..
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(261, 264)

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 0, 131, 111))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/start-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(211, 105))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.start)

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(130, 0, 131, 111))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(103, 178))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.done)

        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(0, 110, 261, 21))
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")

        # self.pushButton_4 = QtWidgets.QPushButton(Form)
        # self.pushButton_4.setGeometry(QtCore.QRect(261, 0, 131, 132))
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("icons/add.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # self.pushButton_4.setIcon(icon)
        # self.pushButton_4.setIconSize(QtCore.QSize(145, 200))
        # self.pushButton_4.setCheckable(False)
        # self.pushButton_4.setObjectName("pushButton_4")
        # self.pushButton_4.clicked.connect(self.add)

        self.label_1 = QtWidgets.QLabel("    Student Details",Form)
        self.label_1.setGeometry(0, 132, 261, 132)
        self.label_1.setObjectName("label1")
        self.label_1.setFont(QFont('Arial', 15))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # def add(self):
    #     #it will open csv file containing records..
    #     record_csv_path = "F://pycharmProjects//Attendance"
    #     subprocess.Popen([record_csv_path, "record.csv"])

    def start(self):
        
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

                    self.label_1.setText(f"Name {name}\n{data.loc[name].to_string()}")
                    self.label_1.setStyleSheet("border: 1px solid black;")
                        
                    cv2.imshow('Webcam',img)
                    cv2.waitKey(1)

    def done(self):
            sys.exit(app.exec_())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form","PRMCEAM"))

if __name__ == "__main__":
            import sys
            app = QtWidgets.QApplication(sys.argv)
            Form = QtWidgets.QWidget()
            ui = Ui_Form()
            ui.setupUi(Form)
            Form.show()
            sys.exit(app.exec_())