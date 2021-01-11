import sys
from PyQt5 import QtCore, QtWidgets
import engine.generalfunction as fn
import engine.databaseFunction as db
import login
import main_window
import register_criminal
import search_criminal
import search_result

#added
import database

class Controller:

    path = "database/"
    db_file = path + "facerecognition.db"
    
    if __name__ == '__main__':
        if(not fn.check_path_exists(db_file)):
            print ('creating db')
            fn.assure_path_exists(path)
            db.create_db(db_file)

    def __init__(self):
        pass

    def show_login(self):
        self.login = login.Ui()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self):
        self.main_window = main_window.Ui()
        self.main_window.switch_register.connect(self.show_register)
        self.main_window.switch_search.connect(self.show_search)
        #added
        self.main_window.switch_database.connect(self.show_database)
        #end
        self.login.close()
        self.main_window.show()

    def show_register(self):
        self.register_criminal = register_criminal.Ui()
        self.register_criminal.show()
    
    def show_search(self):
        self.search_criminal = search_criminal.Ui()
        self.search_criminal.search_result.connect(self.show_result)
        self.search_criminal.show()

    def show_result(self,id,confidence):
        self.search_result = search_result.Ui(id,confidence)
        self.search_result.show()

    #added 13/10/2019
    def show_database(self):
        self.database = database.Ui()
        self.database.switch_user.connect(self.show_result)
        self.database.show()
        self.database.show_all_user_data()
    #end
   
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()