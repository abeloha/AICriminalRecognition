#from PyQt5 import QtWidgets, uic
import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog 
import engine.databaseFunction as db
import engine.generalfunction as fn
import engine.training as tr
import engine.face_recognition as fr

from datetime import datetime

class Ui(QtWidgets.QDialog):

    search_result = QtCore.pyqtSignal(int,int)

    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/search-criminal.ui', self)
        
        self.buttonFile = self.findChild(QtWidgets.QPushButton, 'select_image')
        self.buttonFile.clicked.connect(self.FileButtonPressed) 

        self.button = self.findChild(QtWidgets.QPushButton, 'search_database')
        self.button.clicked.connect(self.SearchButtonPressed) 

        self.image_label = self.findChild(QtWidgets.QLabel, 'image_label')
        self.label_submit_progress = self.findChild(QtWidgets.QLabel, 'label_submit_progress')
        self.label_submit_progress.setText('')
        self.image = ''


    def FileButtonPressed(self): 
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp)") # Ask for file
        if fileName: # If the user gives a file
            self.image = fileName
            pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
            pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
            self.image_label.setPixmap(pixmap) # Set the pixmap onto the label
            self.image_label.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center

    def SearchButtonPressed(self):
        #disable submit botton
        self.button.setDisabled(True)       
        self.label_submit_progress.setText('Please Wait...')
        
        if (
            not self.image
        ):
            msg = QMessageBox()
            msg.setText("Please select an image with a face.")
            msg.setWindowTitle("Select a Picture")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("background-color: rgb(0, 0, 0);")
            msg.setStyleSheet("color: black;")
            msg.exec_()
            self.submit_exit_fxn()
            return
        
        chk = self.check_trainer()
        if (not chk):
            msg = QMessageBox()
            msg.setText("No training data has been entered into the system. \nThe system must learn models before search can be performed. And you'll need more than one sample to learn a model.\n\nTo begin, select Register")
            msg.setWindowTitle("No training model")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("background-color: rgb(0, 0, 0);")
            msg.setStyleSheet("color: black;")
            msg.exec_()
            self.submit_exit_fxn()
            return

        chkrecg,id,confidence,count = fr.face_recognizer(self.image)
        print('chkrecg: ' +str(chkrecg))
        print('id: ' +str(id))
        print('confidence: ' +str(confidence))
        print('count: ' +str(count))  
            
        self.submit_exit_fxn()
        if(id and chkrecg):
            self.search_result.emit(id,confidence)
        
        else:
            
            msg = QMessageBox()
            msg.setText("Sorry, this person is not found in the system. \nSearch with a different picture. Also, ensure the picture you use contains only one face.")
            msg.setWindowTitle("Not found")
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("background-color: rgb(0, 0, 0);")
            msg.setStyleSheet("color: black;")
            msg.exec_()

            self.submit_exit_fxn()
            return



        
   
    def submit_exit_fxn(self):
        self.label_submit_progress.setText('')
        self.button.setDisabled(False)

    def check_trainer(self):
        self.label_submit_progress.setText('Training model first before search!')
        if(not fn.check_path_exists('trainer/trainer.yml')):
            print('training models first')
            chk = tr.trainer()
            return chk
        else:
            return True
