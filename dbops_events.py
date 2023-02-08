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

    #ret = db_cursor.lastrowid
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

### Main ###
try:
    sys.argv[1]

    if sys.argv[1] == 'add':

        try:

            sys.argv[2]

            print(dbAdd(sys.argv[2]))

        except:

            print("Wrong ADD cmd syntaxes - no sys.argv[2]")

    elif sys.argv[1] == 'print-all':

        print(dbPrintAll())

    elif sys.argv[1] == 'del':

        try:

            sys.argv[2]

            print(dbDel(sys.argv[2]))

        except:

            print("Wrong DEL cmd syntaxes - no sys.argv[2]")

    else:

        print("Unknown sys.argv[1]")

except:

    print("Wrong command syntaxes - no sys.argv[1]\n Supports:\n\t print-all \t-print all entries from DB events\n\t add \t\t-Add entry\n\t del \t\t-Delete entry\entries by ID")

