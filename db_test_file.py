
import engine.databaseFunction as db
import engine.generalfunction as fn

from datetime import datetime

if __name__ == '__main__':
    path = "database/"
    db_file = path + "facerecognition.db"
    if(not fn.check_path_exists(db_file)):
        print ('creating db')
        fn.assure_path_exists(path)
        db.create_db(db_file)
        print ('done creating db')
    else:
        print('db already exists')
    
def test_create_user():
    id = 0

    surname      = 'Onuoha'
    firstname    = 'Abel'
    othername    = 'Agu'
    biodata      = "Honest and hard working guy"
    date_created = datetime.now().strftime("%d-%m-%Y %H:%M")
    
  
    data = (surname,firstname,othername,biodata, date_created)

    conn = db.create_connection(db_file)
    if conn is not None:
        with conn:
            id = db.create_users(conn,data)
    else:
        db.conn_error_handle()

    return id

def test_update_user():
    id = 0

    surname      = 'Onuoha2'
    firstname    = 'Abel2'
    othername    = 'Agu2'
    biodata      = "Honest and hard working guy1"
    
    data = (surname,firstname,othername,biodata, 2)

    conn = db.create_connection(db_file)
    if conn is not None:
        with conn:
            id = db.update_users(conn,data)
    else:
        db.conn_error_handle()

    return id

def test_fetch_user():
    a = 3


#id = test_update_user()
#print('inserted id = ' + str(id))
print('end of main')