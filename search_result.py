import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
#input dialog
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit

import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.training as tr
import engine.face_recognition as fr

import add_offense
import edit_criminal
import os


class Ui(QtWidgets.QDialog):

    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self, param_id, param_conf):
        super(Ui, self).__init__()
        uic.loadUi('ui/search-result.ui', self)
        self.id = param_id
        self.conf = param_conf

        self.deleteBtn = self.findChild(QtWidgets.QPushButton, 'deleteBtn')
        self.deleteBtn.clicked.connect(self.deleteButtonPressed)

        self.add_offenceBtn = self.findChild(QtWidgets.QPushButton, 'add_offenceBtn')
        self.add_offenceBtn.clicked.connect(self.add_offenceButtonPressed)

        self.editBtn = self.findChild(QtWidgets.QPushButton, 'editBtn')
        self.editBtn.clicked.connect(self.editButtonPressed)

        self.name = self.findChild(QtWidgets.QLabel, 'name')
        self.confidence = self.findChild(QtWidgets.QLabel, 'confidence')
        self.marital_status = self.findChild(QtWidgets.QLabel, 'marital_status')
        self.biodata_area = self.findChild(QtWidgets.QScrollArea, 'biodata_area')

        self.dob = self.findChild(QtWidgets.QLabel, 'dob')
        self.photo = self.findChild(QtWidgets.QLabel, 'photo')
        self.photo_2 = self.findChild(QtWidgets.QLabel, 'photo_2')
        self.photo_3 = self.findChild(QtWidgets.QLabel, 'photo_3')
        self.photo_4 = self.findChild(QtWidgets.QLabel, 'photo_4')

        self.display_user_data()
        self.display_offense_data()

        self.show()

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
        self.confidence.setText("{0:.2f}%".format(round(100 - self.conf, 2)))
        self.marital_status.setText(marital_status)
        self.dob.setText(dob)

        #biodata
        message_label = QtWidgets.QLabel()
        message_label.setWordWrap(True)
        message_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)        
        message_label.setText(biodata)
        message_label.setFixedWidth(self.biodata_area.width()-20)
        message_label.setContentsMargins(10, 10, 10, 0)
        self.biodata_area.setWidget(message_label)

        #set photo
        fileName = "data_images/User." + str(self.id) + '.' + str(1) + ".jpg"
        if os.path.exists(fileName):
            self.image = fileName
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.photo.width(), self.photo.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.photo.setPixmap(pixmap) # Set the pixmap onto the label
            self.photo.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center

        fileName = "data_images/User." + str(self.id) + '.' + str(2) + ".jpg"
        if os.path.exists(fileName):
            self.image = fileName
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.photo_2.width(), self.photo_2.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.photo_2.setPixmap(pixmap) # Set the pixmap onto the label
            self.photo_2.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center
        
        fileName = "data_images/User." + str(self.id) + '.' + str(3) + ".jpg"
        if os.path.exists(fileName):
            self.image = fileName
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.photo_3.width(), self.photo_3.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.photo_3.setPixmap(pixmap) # Set the pixmap onto the label
            self.photo_3.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center

        fileName = "data_images/User." + str(self.id) + '.' + str(4) + ".jpg"
        if os.path.exists(fileName):
            self.image = fileName
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.photo_4.width(), self.photo_4.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.photo_4.setPixmap(pixmap) # Set the pixmap onto the label
            self.photo_4.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center

        if not c:
            self.show_message('Deleted Record','This data has been deleted from the system.')
              
    def display_offense_data(self):
        offenses = self.load_offense_data() 
        message_label = QtWidgets.QLabel()
        message_label.setWordWrap(True)
        message_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        message_label_text = ''

        c = 1
        for d in offenses:
            message_label_text += str(c) + ". " + "<strong>" +d[2]+ "</strong>:<br>"
            message_label_text += d[3] + "<br><br>"            
            c+=1

        message_label.setText(message_label_text)
        message_label.setFixedWidth(self.offense_area.width()-20)
        message_label.setContentsMargins(10, 10, 10, 0)
        self.offense_area.setWidget(message_label)       
        
    def load_user_data(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_users(conn,self.id)
        else:
            db.conn_error_handle()

        return data

    def load_offense_data(self):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_offense(conn,self.id)
        else:
            db.conn_error_handle()

        return data

    def deleteButtonPressed(self):
        text, okPressed = QInputDialog.getText(self, "Enter Password","To delete this data, you must enter password\nEnter Password:", QLineEdit.Password, "")
        if okPressed:
            if (text != ''):
                auth = self.check_password(str(text))
                if auth:
                    self.delete_users(self.id)
                    self.show_message('User Deleted', 'This user has been deleted from the system. \nYou must retrain system before the sytem can stop recorgnising his/her face')
                else:
                    self.show_message('Wrong Password', 'The password you entered is incorrect')
            else:
                self.show_message('No password entered', 'No value entered. You must enter a password')

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
    
    def delete_users(self,id):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                db.delete_users(conn,id)
        else:
            db.conn_error_handle()  

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(0, 0, 0);")
        msg.setStyleSheet("color: black;")
        msg.exec_()

    def add_offenceButtonPressed(self):
        self.add_offense = add_offense.Ui(self.id)
        self.add_offense.switch_user.connect(self.result_close)
        self.add_offense.show()

    def result_close(self, user_id):
        self.close()

    def editButtonPressed(self):
        self.edit_criminal = edit_criminal.Ui(self.id)
        self.edit_criminal.switch_user.connect(self.result_close)
        self.edit_criminal.show()


