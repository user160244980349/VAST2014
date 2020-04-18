import sqlite3


connection = None
cursor = None


def connect(db):

    try:
        global connection
        global cursor

        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        print("Database successfully connected to SQLite")

        query = "select sqlite_version();"
        cursor.execute(query)
        record = cursor.fetchall()
        print("SQLite Database Version is:", record)

        query = "PRAGMA foreign_keys = ON;"
        cursor.execute(query)

    except sqlite3.Error as error:
        print("Error while connecting to sqlite: ", error)


def disconnect():

    try:
        global connection
        global cursor

        connection.commit()
        connection.close()
        print("The SQLite connection is closed")

    except sqlite3.Error as error:
        print("Error while connecting to sqlite:", error)


def execute(query):

    try:
        global connection
        global cursor

        cursor.execute(query)
        records = cursor.fetchall()
        return records

    except sqlite3.Error as error:
        print("Error while connecting to sqlite:", error)
