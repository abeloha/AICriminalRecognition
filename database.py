#from PyQt5 import QtWidgets, uic
import sys, copy
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import engine.databaseFunction as db
import engine.generalfunction as fn


class Ui(QtWidgets.QDialog):

    switch_user = QtCore.pyqtSignal(int,int)

    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/database.ui', self)

        self.table_area = self.findChild(QtWidgets.QScrollArea, 'table_area')

        self.searchBtn = self.findChild(QtWidgets.QPushButton, 'searchBtn') 
        self.searchBtn.clicked.connect(self.searchButtonPressed) 

        self.search_text = self.findChild(QtWidgets.QLineEdit, 'search_text')
        self.label_progress = self.findChild(QtWidgets.QLabel, 'label_progress')

        self.label_progress.hide()

    def show_all_user_data(self,name=''):
        self.label_progress.show()
        self.label_progress.setText('Loading...')
        data = self.load_users(name)
        self.creating_tables(data)


    def searchButtonPressed(self):
        search_text = self.search_text.text()
        print('searching for: ' + search_text)
        self.show_all_user_data(search_text)

    def switch_to_user(self, user_id):
        confidence = 0
        self.switch_user.emit(user_id, confidence)

    def load_users(self, name = ''):
        data = ()
        conn = db.create_connection(self.db_file)
        if conn is not None:
            with conn:
                data = db.get_users_by_name(conn,name)
        else:
            db.conn_error_handle()

        return data
        
    def creating_tables(self, data):
        self.tableWidget = QTableWidget()
        
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(("id;surname;firstname;othername;status;DOB;action").split(";"))
        self.tableWidget.setColumnHidden(0,True)      
            
        c = 0
        for d in data:
            user_id = d[0]
            surname = d[1]
            firstname = d[2]
            othername = d[3]
            biodata = d[4]
            dob = d[5]
            marital_status = d[6]
            self.tableWidget.setItem(c, 0 , QTableWidgetItem(str(user_id))) 
            self.tableWidget.setItem(c, 1 , QTableWidgetItem(surname))
            self.tableWidget.setItem(c, 2 , QTableWidgetItem(firstname))
            self.tableWidget.setItem(c, 3 , QTableWidgetItem(othername))
            self.tableWidget.setItem(c, 4 , QTableWidgetItem(marital_status))
            self.tableWidget.setItem(c, 5 , QTableWidgetItem(dob))
            self.tableWidget.setItem(c, 6 , QTableWidgetItem('view'))  
            c+=1
        
         # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
        
        self.table_area.setWidget(self.tableWidget)

        self.label_progress.setText('')
        self.label_progress.hide()

    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            row = currentQTableWidgetItem.row()
        
        item = self.tableWidget.item(row, 0)
        user_id = int(item.text())
        self.switch_to_user(user_id)


        #print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

            
