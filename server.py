# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time, socket, sys
import threading

conn = None
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Servidor")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(23, 96, 135, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_iniciar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_iniciar.setGeometry(QtCore.QRect(100, 60, 131, 61))
        self.btn_iniciar.setObjectName("btn_iniciar")
        self.btn_iniciar.setStyleSheet("font: 8pt \"Segoe UI\";\n""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgb(0, 159, 183));")
        self.btn_iniciar.clicked.connect(lambda:self.start())
        self.btn_enviar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_enviar.setGeometry(QtCore.QRect(580, 380, 131, 41))
        self.btn_enviar.setStyleSheet("font: 8pt \"Segoe UI\";\n""background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgb(0, 159, 183));")
        self.btn_enviar.setObjectName("btn_enviar")
        self.btn_enviar.clicked.connect(lambda:self.send())
        self.txt_send = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_send.setGeometry(QtCore.QRect(100, 370, 441, 61))
        self.txt_send.setObjectName("txt_send")
        self.txt_send.setStyleSheet("font: 8pt \"Segoe UI\";\n"
                                     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(172, 189, 186, 255));")
        self.txt_recv = QtWidgets.QTextBrowser(self.centralwidget)
        self.txt_recv.setGeometry(QtCore.QRect(100, 170, 441, 141))
        self.txt_recv.setObjectName("txt_recv")
        self.txt_recv.setStyleSheet("font: 8pt \"Segoe UI\";\n"
                                     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgba(172, 189, 186, 255));")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.threadpool = QtCore.QThreadPool()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_iniciar.setText(_translate("MainWindow", "Start Server"))
        self.btn_enviar.setText(_translate("MainWindow", "Send"))
            
    
    def updateMsg(self,text):
        self.txt_recv.setText(self.txt_recv.toPlainText()+"\n"+text)
    
    def start(self):
        self.txt_recv.setText("Starting server...")
        time.sleep(1)
        host = "127.0.0.1"
        ip = socket.gethostbyname(host)
        port = 4445
        server_socket.bind((host, port))
        server_socket.listen(5)
        self.updateMsg("searching for connections...")
        connector, addr = server_socket.accept()
        self.txt_recv.setText("Server has Join the chat")
        self.updateMsg("Client has join the chat")
        global conn
        conn = connector
        self.l = listener()
        self.l.txt.connect(self.updateMsg)
        self.l.start()
        self.btn_iniciar.setDisabled(True)
        
    def send (self):
        message = self.txt_send.toPlainText()
        if message == "": return
        self.updateMsg("Server says: " + message)
        conn.send(message.encode())
        self.txt_send.setText("")
        
class listener(QtCore.QThread):
    running = True
    txt = QtCore.pyqtSignal(str)
    
    def run(self):
        while self.running:
            global conn
            message = conn.recv(1024)
            message = message.decode()
            message = "Client says: " + message
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
   
    
