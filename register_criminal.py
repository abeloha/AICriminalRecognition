#from PyQt5 import QtWidgets, uic
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog 
import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.face_datasets as ds
import engine.training as tr

from datetime import datetime

class Ui(QtWidgets.QDialog):
    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/register-criminal.ui', self)

        
        self.buttonFolder = self.findChild(QtWidgets.QPushButton, 'folder_select') # Find the button
        self.buttonFolder.clicked.connect(self.folderButtonPressed) # Remember to pass the definition/method, not the return value!

        self.button = self.findChild(QtWidgets.QPushButton, 'submit') # Find the button
        self.button.clicked.connect(self.submitButtonPressed) # Remember to pass the definition/method, not the return value!

        self.surname = self.findChild(QtWidgets.QLineEdit, 'surname')
        self.firstname = self.findChild(QtWidgets.QLineEdit, 'firstname')
        self.othername = self.findChild(QtWidgets.QLineEdit, 'othername')
        self.marital_status = self.findChild(QtWidgets.QComboBox, 'marital_status')
        self.dob = self.findChild(QtWidgets.QDateEdit, 'dob')
        self.biodata = self.findChild(QtWidgets.QTextEdit, 'biodata')
        self.offense = self.findChild(QtWidgets.QTextEdit, 'offense')
        self.offense_date = self.findChild(QtWidgets.QDateEdit, 'offense_date')
        self.train_system_now = self.findChild(QtWidgets.QCheckBox, 'train_system_now')
        self.label_select_folder = self.findChild(QtWidgets.QLabel, 'label_select_folder')
        self.label_submit_progress = self.findChild(QtWidgets.QLabel, 'label_submit_progress')
        self.imageFolder = ''

        self.label_select_folder.setText('')
        self.label_submit_progress.setText('')


    def folderButtonPressed(self):
        self.imageFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.label_select_folder.setText(self.imageFolder)

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
        offense = self.offense.toPlainText()
        offense_date = self.offense_date.date().toString("dd/MM/yyyy")
        imageFolder = self.imageFolder
        
        if (
            not surname or not firstname or not offense
        ):
            QMessageBox.warning(self, "Missing fields", "Please fill all the input with (*) \nThey are required. Thanks")
            self.submit_exit_fxn()
            return

        if (
            not imageFolder
        ):
            QMessageBox.warning(self, "Missing image folder", "Please select an image folder \nThis folder will be used to learn to recorgnise this person.")
            self.submit_exit_fxn()
            return   

        date_created = datetime.now().strftime("%d-%m-%Y %H:%M") 
        self.data = (surname,firstname,othername,marital_status,dob,biodata, date_created)
        id = self.insert_user()

        if(id):
            print('inserted id: ' + str(id))

            number_of_faces = self.prepare_face_dataset(id,self.imageFolder)
            if(number_of_faces > 2):

                #insert the offense
                self.offence_data = (id,offense,offense_date, date_created)
                offence_id = self.insert_offense()

                if(self.train_system_now.isChecked()):
                    print ('Training Model Now')
                    tr.trainer()

                buttonReply = QMessageBox.question(self, 'Sucesses', "This profile has been added successfully.\nDo you want to add another?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    self.clear_all_input()
                else:
                    self.close()

            else:
                print('no face detected, record will be removed')
                self.delete_users(id)
                QMessageBox.critical(self, "No face found", "Please note that there is a problem leaning this data.\nThere are no two distinct faces found in the folder you selected, so this profile is not created.\nThe system needs at least two faces to learn how to recognise this person")


        self.submit_exit_fxn()
                
    def submit_exit_fxn(self):
        #enable submit botton
        self.label_submit_progress.setText('')
        self.button.setDisabled(False)
     
    def insert_user(self):
        id = 0
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                id = db.create_users(conn,self.data)
        else:
            db.conn_error_handle()

        return id
    
    def delete_users(self,id):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                db.delete_users(conn,id)
        else:
            db.conn_error_handle()   

    def insert_offense(self):
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                id = db.create_offense(conn,self.offence_data)
        else:
            db.conn_error_handle()

        return id
    
    def prepare_face_dataset(self,id,path):
        print(path)
        return ds.execute_face_datasets(id,path)

    def clear_all_input(self):
        self.surname.setText('')
        self.firstname.setText('')
        self.othername.setText('')
        self.marital_status.setCurrentIndex(0)
        self.biodata.setPlainText('')
        self.offense.setPlainText('')
        self.imageFolder = ''
        self.label_select_folder.setText(self.imageFolder)
