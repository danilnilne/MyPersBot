import sys
import datetime
import bot_conf
import mysql.connector

event = sys.argv[1]
### dbConnect: use settings from config and connect t DB. Returns db_cursor
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

        for (id, timestamp, description) in db_cursor:

            print("{}\t | {}\t | {}\t ".format(id, timestamp, description))

        db_cursor.close()

        db_data["db_connect"].close()

    else:

        return db_data["error"]
### dbRequest: END

### dbAdd:
def dbAdd(event):

    db_data = dbConnect();

    if db_data["returncode"] == 0:

        db_cursor = db_data["db_connect"].cursor()

        query = ("INSERT INTO events""(timestamp, description) ""VALUES (%s, %s)")

        insert_data = (datetime.datetime.now(), event)

        db_cursor.execute(query, insert_data)

        db_data["db_connect"].commit()

        ret = 0

        db_cursor.close()

        db_data["db_connect"].close()

    else:

        ret =  db_data["error"];

    return ret;
### dbAdd: END

dbAdd(event)
