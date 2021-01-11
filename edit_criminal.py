import sys
from PyQt5.QtCore  import QDate
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
        uic.loadUi('ui/edit-criminal.ui', self)
        self.id = param_id
    
        self.button = self.findChild(QtWidgets.QPushButton, 'submit') # Find the button
        self.button.clicked.connect(self.submitButtonPressed) # Remember to pass the definition/method, not the return value!

        self.surname = self.findChild(QtWidgets.QLineEdit, 'surname')
        self.firstname = self.findChild(QtWidgets.QLineEdit, 'firstname')
        self.othername = self.findChild(QtWidgets.QLineEdit, 'othername')
        self.marital_status = self.findChild(QtWidgets.QComboBox, 'marital_status')
        self.dob = self.findChild(QtWidgets.QDateEdit, 'dob')
        self.biodata = self.findChild(QtWidgets.QTextEdit, 'biodata')
        self.label_submit_progress = self.findChild(QtWidgets.QLabel, 'label_submit_progress')

        self.label_submit_progress.setText('')       


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

        self.surname.setText(surname)
        self.firstname.setText(firstname)
        self.othername.setText(othername)

        index = self.marital_status.findText(marital_status, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.marital_status.setCurrentIndex(index)

        edob = dob.split('/')
        ndob = edob[2] + '-' + edob[1] + '-' + edob[0]
        qtDate = QtCore.QDate.fromString(ndob, 'yyyy-MM-dd')

        #self.dob.setDate(.setDate(QtCore.QDate(now.year, now.month, now.day)))        
        self.dob.setDate(QtCore.QDate(qtDate.year(), qtDate.month(), qtDate.day()))
        self.biodata.setText(biodata)

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

    def submitButtonPressed(self):
        #disable submit botton
        self.button.setDisabled(True)       
        self.label_submit_progress.setText('Please Wait...')
        surname = self.surname.text()
        firstname = self.firstname.text()
        othername = self.othername.text()
        marital_status = self.marital_status.currentText()
        dob = self.dob.date().toString("dd/MM/yyyy")
        biodata = self.biodata.toPlainText()   
         
        
        if (
            not surname or not firstname
        ):
            QMessageBox.warning(self, "Missing fields", "Please fill all the input with (*) \nThey are required. Thanks")
            self.submit_exit_fxn()
            return
        
        date_created = datetime.now().strftime("%d-%m-%Y %H:%M") 
        self.data = (surname,firstname,othername,biodata, marital_status, dob, self.id)
        self.edit_user()
        self.submit_exit_fxn()

        self.search_result = search_result.Ui(self.id,0)
        self.switch_user.emit(self.id)
        self.search_result.show()
        self.close()

    def submit_exit_fxn(self):
            #enable submit botton
        self.label_submit_progress.setText('')
        self.button.setDisabled(False)
     
    def edit_user(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                db.update_users(conn,self.data)
        else:
            db.conn_error_handle()
