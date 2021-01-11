import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
#input dialog
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.training as tr
import engine.face_recognition as fr

import os
from datetime import datetime

import search_result


class Ui(QtWidgets.QDialog):

    switch_user = QtCore.pyqtSignal(int)

    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_id):
        super(Ui, self).__init__()
        uic.loadUi('ui/add-offense.ui', self)
        self.id = param_id
    
        self.add_offenceBtn = self.findChild(QtWidgets.QPushButton, 'add_offenceBtn')
        self.add_offenceBtn.clicked.connect(self.add_offenceButtonPressed)

        self.offense = self.findChild(QtWidgets.QTextEdit, 'offense')
        self.offense_date = self.findChild(QtWidgets.QDateEdit, 'offense_date')

        self.name = self.findChild(QtWidgets.QLabel, 'name')        


        self.display_user_data()


    def display_user_data(self):
        user_data = self.load_user_data()
        surname = ''; firstname = ''; othername = ''; biodata = ''; dob = ''; marital_status = ''
        
        c = 0
        for d in user_data:
            if(d[1]):
                surname = d[1]
            if(d[2]):
                firstname = d[2]
            if(d[3]):
                othername = d[3]
            if(d[4]):
                biodata = d[4]
            if(d[5]):
                dob = d[5]
            if(d[6]):
                marital_status = d[6]
            c = 1

        self.name.setText(surname + ' ' + firstname + ' ' + othername)
        

        if not c:
            self.show_message('Deleted Record','This data has been deleted from the system.')
              
    def load_user_data(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_users(conn,self.id)
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

    def add_offenceButtonPressed(self):

        offense = self.offense.toPlainText()
        offense_date = self.offense_date.date().toString("dd/MM/yyyy")
        date_created = datetime.now().strftime("%d-%m-%Y %H:%M") 

        offence_data = (self.id,offense,offense_date, date_created)
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                id = db.create_offense(conn,offence_data)
        else:
            db.conn_error_handle()

        self.search_result = search_result.Ui(self.id,0)

        self.switch_user.emit(self.id)

        self.search_result.show()
        self.close()

