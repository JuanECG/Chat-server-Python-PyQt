# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cliente.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time, socket, sys
import threading

s = socket.socket()
conn = None
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Cliente")
        MainWindow.resize(750, 500)
        MainWindow.setStyleSheet("")
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(20, 115, 50, 1));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_conectar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_conectar.setGeometry(QtCore.QRect(100, 60, 131, 61))
        self.btn_conectar.setObjectName("btn_conectar")
        self.btn_conectar.setStyleSheet("font: 8pt \"Segoe UI\";\n""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgb(119, 156, 171));")
        self.btn_conectar.clicked.connect(lambda:self.connect())
        self.btn_enviar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_enviar.setGeometry(QtCore.QRect(580, 380, 131, 41))
        self.btn_enviar.setObjectName("btn_enviar")
        self.btn_enviar.setStyleSheet("font: 8pt \"Segoe UI\";\n""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgb(119, 156, 171));")
        self.btn_enviar.clicked.connect(lambda:self.send())
        self.bnt_buscar = QtWidgets.QPushButton(self.centralwidget)
        self.bnt_buscar.setGeometry(QtCore.QRect(580,60,131,61))
        self.bnt_buscar.setStyleSheet("font: 8pt \"Segoe UI\";\n""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgb(119, 156, 171));")
        self.bnt_buscar.setObjectName("btn_buscar")
        self.bnt_buscar.setEnabled(False)
        self.btn_enviar.setEnabled(False)
        self.bnt_buscar.clicked.connect(lambda:self.search())
        self.txt_send = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_send.setGeometry(QtCore.QRect(100, 370, 441, 61))
        self.txt_send.setObjectName("txt_send")
        self.txt_send.setStyleSheet("font: 8pt \"Segoe UI\";\n"
                                     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(162, 232, 221, 1));")
        self.txt_recv = QtWidgets.QTextBrowser(self.centralwidget)
        self.txt_recv.setGeometry(QtCore.QRect(100, 170, 441, 141))
        self.txt_recv.setObjectName("txt_recv")
        self.txt_recv.setStyleSheet("font: 8pt \"Segoe UI\";\n"
                                     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(162, 232, 221, 1));")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #MainWindow.setStyleSheet(open('styles.css').read())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Cliente"))
        self.btn_conectar.setText(_translate("MainWindow", "Connect"))
        self.btn_enviar.setText(_translate("MainWindow", "Send"))
        self.bnt_buscar.setText(_translate("MainWindow","Search"))  
        
    def updateMsg(self,text):
        if text[13:21] == '|RESULT|':
            self.txt_send.setText(self.txt_send.toPlainText() + ' ' +text[21:] )
            return
            
        self.txt_recv.setText(self.txt_recv.toPlainText()+"\n"+text)
        
    def send(self):
        message = self.txt_send.toPlainText()
        if message == "": return
        self.updateMsg("Client says: " + message)
        s.send(message.encode())
        self.txt_send.setText("")
        
    def connect(self):
        #shost = socket.gethostname()
        #ip = socket.gethostbyname(shost)
        host = "NONE"
        port = 4445
        #self.txt_recv.setText("Trying to connect to "+ host+ "("+ str(port) +")\n")
        #self.txt_recv.setText("Trying to connect to "+ host+ "("+ port +")\n")
        time.sleep(1)
        try:
            s.connect((host, port))        
        except:
            self.txt_recv.setText(self.txt_recv.toPlainText() + "\nConnection error")
            return
        self.txt_recv.setText("Server has join the chat")
        self.updateMsg("Client has join the chat")
        #s.send(b"Client has join the chat")
        self.l = listenerClient()
        self.l.txt.connect(self.updateMsg)
        self.l.start()
        self.btn_conectar.setDisabled(True)
        self.btn_enviar.setEnabled(True)
        self.bnt_buscar.setEnabled(True)
        
    def search(self):
        message = '|QUERY|'+self.txt_send.toPlainText()
        s.send(message.encode())
        
class listenerClient(QtCore.QThread):
    running = True
    txt = QtCore.pyqtSignal(str)
    
    def run(self):
        while self.running:
            message = s.recv(1024)
            message = message.decode()
            message = "Server Says: " + message
            self.txt.emit(message)
            time.sleep(1)
    def stop(self):
        self.running = False      
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    

    sys.exit(app.exec_())

