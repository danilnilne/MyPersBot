import os
import mysql.connector as database

username = 'admin'
password = 'Unix0stream'

connection = database.connect(
    user=username,
    password=password,
    host='localhost',
    charset='utf8',
    database='kds.local')

cursor = connection.cursor()

def get_data(id):
    try:
      statement = "SELECT * FROM events WHERE id=%s"
      data = (id,)
      cursor.execute(statement, data)
      for (id, timestamp, event) in cursor:
        print(f"Successfully retrieved {id}, {timestamp}, {event}")
    except database.Error as e:
      print(f"Error retrieving entry from database: {e}")

get_data(225)

connection.close()
