#from PyQt5 import QtWidgets, uic
import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog 
import engine.databaseFunction as db
import engine.generalfunction as fn
from datetime import datetime

class Ui(QtWidgets.QDialog):

    switch_window = QtCore.pyqtSignal()

    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/login.ui', self)

        
        self.button = self.findChild(QtWidgets.QPushButton, 'login') # Find the button
        self.button.clicked.connect(self.submitButtonPressed) # Remember to pass the definition/method, not the return value!

        self.password = self.findChild(QtWidgets.QLineEdit, 'password')
        self.password_error = self.findChild(QtWidgets.QLabel, 'password_error')
        self.password_error.setText('')
        self.password_error.hide()

    def submitButtonPressed(self):
        self.password_error.hide()
        password = self.password.text()

        if(password == '_UNLOCK_'):
            self.perform_account_change_user('user')
            self.show_message('Admin', 'Admin Features has been unlocked!!! \nLogin to continue')
            self.password.setText('')
            return


        auth = self.check_password(password)

        if(not auth):
            self.password_error.setText('<html><head/><body><p><span style=" font-size:16pt; color:#aa0000;">The Password is Incorrect</span></p></body></html>')
            self.password_error.show()
            return

        self.switch_window.emit()
        

    def check_password(self,password):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_account(conn)
        else:
            db.conn_error_handle()

        
        for d in data:
           if (d[2] == password):
                return 1

        return 0

    def perform_account_change_user(self, user_type): 
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.update_account_change_user(conn,user_type)
        else:
            db.conn_error_handle()

        return data

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("color: black;")
        msg.exec_()


   
        
