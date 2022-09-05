from __future__ import print_function
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
from scipy.signal import argrelextrema
import numpy as np

import wave



import sys
import os.path 
from io import StringIO


Nota22 = StringIO()  
nota= []
Nota2 = StringIO()
class Ui_Form(object):
   
    def setupUi(self, Form):
        
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.setEnabled(True)
        Form.resize(1280, 720)
        Form.setSizeIncrement(QtCore.QSize(16, 9))
        Form.setMouseTracking(False)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setSizeGripEnabled(False)
        
        self.openGLWidget = QtWidgets.QLabel(Form)
        self.openGLWidget.setStyleSheet("background-color: yellow") 
        self.openGLWidget.setEnabled(True)
        self.openGLWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        
        
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        
        
        font.setPointSize(26)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.openGLWidget.setFont(font)
        self.openGLWidget.setText("        Waiting for the song ...")
        self.openGLWidget.setGeometry(QtCore.QRect(310, 90, 720, 260))
        self.openGLWidget.setObjectName("openGLWidget")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(480, 350, 351, 131))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(3)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton.setMouseTracking(False)
        self.pushButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.pushButton.setAcceptDrops(False)
        self.pushButton.setToolTip("")
        self.pushButton.setToolTipDuration(0)
        self.pushButton.setWhatsThis("")
        self.pushButton.setAccessibleName("")
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/home.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(350, 3000))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(True)
        self.pushButton.setProperty("asdsa","")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAcceptDrops(False)
        self.label.setAutoFillBackground(False)
        self.label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/test.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.openGLWidget.raise_()
        self.label.raise_()
        self.pushButton.raise_()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Music Interpreter"))
        self.label.setToolTip(_translate("Form", "<html><head/><body><p><img src=\":/backend/studioo.jpg\"/><img src=\":/newPrefix/studio-2.png\"/></p></body></html>"))
        self.pushButton.clicked.connect(self.pushButton_handler)
       

    def pushButton_handler(self):
        self.open_dialog_box()
    
        
    def open_dialog_box(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " Data File", '.', "(*.wav)")
        path = filename[0]        
        if path == True:
            with open(path, "r") as f:
                print(f.readline())
 
        # ==============================================
        
        time_period = 0.5 # FFT time period (in seconds).
        
        # ==============================================
        
        fs_rate, signal_original = wavfile.read(filename)
        total_time = int(np.floor(len(signal_original)/fs_rate))
        sample_range = np.arange(0,total_time,time_period)
        total_samples = len(sample_range)
        audio_file = wave.open(filename)
        file_length=audio_file.getnframes() 
        
        
        for i in sample_range:
           
            
            sample_start = int(i*fs_rate)
            sample_end = int((i+time_period)*fs_rate)
            signal = signal_original[sample_start:sample_end]
            filelen=file_length/total_time
            l_audio = len(signal.shape)
           
            
            if l_audio == 2:
                signal = signal.sum(axis=1) / 2
            N = signal.shape[0]
           
        
            secs = N / float(fs_rate)
           
            Ts = 1.0/fs_rate # sampling interval in time
           
        
          
            fourier = np.fft.fft(signal)
            fourier = np.absolute(fourier)
            imax=np.argmax(fourier[0:int(filelen/2)]) #index of max element
        	
            #peak detection
            i_begin = -1
            threshold = 0.3 * fourier[imax]
            for i in range (0,imax+100):
                if fourier[i] >= threshold:
                    if(i_begin==-1):
                        i_begin = i				
                if(i_begin!=-1 and fourier[i]<threshold):
                    break
            i_end = i
            imax = np.argmax(fourier[0:i_end+100])
            freq=(imax*Ts)/(Ts*l_audio) #formula to convert index into sound frequency
         
            name = np.array([" ","C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G2#","A2","A2#","B2","C3","C3#","D3","D3#","E3","F3","F3#","G3","G3#","A3","A3#","B3","C4","C4#","D4","D4#","E4","F4","F4#","G4","G4#","A4","A4#","B4","C5","C5#","D5","D5#","E5","F5","F5#","G5","G5#","A5","A5#","B5","C6","C6#","D6","D6#","E6","F6","F6#","G6","G6#","A6","A6#","B6","C7","C7#","D7","D7#","E7","F7","F7#","G7","G7#","A7","A7#","B7","C8","C8#","D8","D8#","E8","F8","F8#","G8","G8#","A8","A8#","B8","Beyond B8"," "])
            frequencies = np.array([16.34,16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96	,27.50	,29.14	,30.87	,32.70	,34.65	,36.71	,38.89	,41.20	,43.65	,46.25	,49.00	,51.91	,55.00	,58.27	,61.74	,65.41	,69.30	,73.42	,77.78	,82.41	,87.31	,92.50	,98.00	,103.83	,110.00	,116.54	,123.47	,130.81	,138.59	,146.83	,155.56	,164.81	,174.61	,185.00	,196.00	,207.65	,220.00	,233.08	,246.94	,261.63	,277.18	,293.66	,311.13	,329.63	,349.23	,369.99	,392.00	,415.30	,440.00	,466.16	,493.88	,523.25	,554.37	,587.33	,622.25	,659.26	,698.46	,739.99	,783.99	,830.61	,880.00	,932.33	,987.77	,1046.50	,1108.73	,1174.66	,1244.51	,1318.51	,1396.91	,1479.98	,1567.98	,1661.22	,1760.00	,1864.66	,1975.53	,2093.00	,2217.46	,2349.32	,2489.02	,2637.02	,2793.83	,2959.96	,3135.96	,3322.44	,3520.00	,3729.31	,3951.07	,4186.01	,4434.92	,4698.64	,4978.03	,5274.04	,5587.65	,5919.91	,6271.93	,6644.88	,7040.00	,7458.62	,7902.13,8000,8100])
            for i in range(0,frequencies.size-1):
                if(freq<frequencies[0]):
                        note=name[0]
                        break
                if(freq>frequencies[-1]):
                    note=name[-1]
                    break
                if freq>=frequencies[i] and frequencies[i+1]>=freq :
                    if freq-frequencies[i]<(frequencies[i+1]-frequencies[i])/2 :
                        note=name[i]
                    else :
                            note=name[i+1]
                
                    break	
            
            nota.append(note)
            nota[0]='                     '
    
            
        while("," in nota):
            nota.remove(",")
            
        for i in range(len(nota)):
                nota[i]+=' '
                if(i%40==0 and i!=0):
                    nota[i]+=' | '
                    nota[i]+='                     '
        temp= ''
        print(nota)
        sait=''.join(nota)
        for a in range(len(sait)):
            temp+=sait[a]
            if(temp[a] == '|'):
                temp+='\n' 
        #     Nota2.write(" "+ note)
         
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.openGLWidget.setText(temp)   
        font.setPointSize(8)
        font.setItalic(True)
        font.setWeight(75)
        self.openGLWidget.setFont(font)    
        del nota[0:999]
        
       

import backend_rc

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QDialog()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    app.exec_()