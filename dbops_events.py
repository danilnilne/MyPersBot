import sys
import datetime
import bot_conf
import mysql.connector

### dbConnect: use settings from config and connect to DB. Returns db_cursor
def dbConnect():

    db_config = {
        'user': bot_conf.db_user,
        'password' : bot_conf.db_password,
        'host' : bot_conf.db_host,
        'charset' : 'utf8',
        'database' : bot_conf.db_name
        }

    try:
        db_connect = mysql.connector.connect(**db_config)

        ret = {"returncode": 0, "db_connect": db_connect, "error": ''}

    except mysql.connector.Error as err:

        ret = {"returncode": 1, "cursor": '', "error": err}

    return ret;
### dbConnect: END

### dbRequest:
def dbPrintAll():

    db_data = dbConnect();

    if db_data["returncode"] == 0:

        db_cursor = db_data["db_connect"].cursor()

        query = ("SELECT * FROM events")

        db_cursor.execute(query)

        for (id, timestamp, description) in db_cursor :

            print("{}\t | {}\t | {}\t ".format(id, timestamp, description))

        ret = 0

        db_cursor.close()

        db_data["db_connect"].close()

    else:

        ret = db_data["error"]

    return ret
### dbRequest: END

### dbAdd:
def dbAdd(event=''):

    db_data = dbConnect();

    if db_data["returncode"] == 0:

        db_cursor = db_data["db_connect"].cursor()

        query = ("INSERT INTO events""(timestamp, description) ""VALUES (%s, %s)")

        insert_data = (datetime.datetime.now(), event)

        db_cursor.execute(query, insert_data)

        ret = 0

        db_data["db_connect"].commit()

        db_cursor.close()

        db_data["db_connect"].close()

    else:

        ret =  db_data["error"];

    return ret;
### dbAdd: END

### dbDel:
def dbDel(id):

    db_data = dbConnect();

    if db_data["returncode"] == 0:

        db_cursor = db_data["db_connect"].cursor()

        if id != "all":

            query = ("DELETE FROM events WHERE id="+id)

        else:

            query = ("TRUNCATE TABLE events")

        try:

            db_cursor.execute(query)

            ret = 0

        except mysql.connector.Error as error:

            ret = error

        db_data["db_connect"].commit()

        db_cursor.close()

        db_data["db_connect"].close()

    else:

        ret =  db_data["error"];

    return ret;
### dbDel: END

### helpPrint()

def helpPrint():
    
    print('''Incorrect command syntax - there is no any args
            Supports:
            --list\t - print all entries from DB events
            --add\t - add entry. --add "<event_message>"
            --del\t - delete entry\entries by ID. Put "<ID>" to delete single ID or "all" to truncate whole Table "Events" 
            ''')

### helpPrint: END

### Main ###
try:
    sys.argv[1]

    if sys.argv[1] == '--add':

        try:

            sys.argv[2]

            print(dbAdd(sys.argv[2]))

        except:

            print("Incorrect command syntax. \"--add\" requires second arg")

    elif sys.argv[1] == '--list':

        print(dbPrintAll())

    elif sys.argv[1] == '--del':

        try:

            sys.argv[2]

            print(dbDel(sys.argv[2]))

        except:

            print("Incorrect command syntax. \"--del\" requires second arg")

    else:

        helpPrint ();

except:

    helpPrint ();