import sqlite3
from sqlite3 import Error
import time


# create the connection with the database. If there is no db, it creates a new one
# @parameter: path of the database (.db file)
# @return: connection object
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


# execute the create table statement using a cursor from the connection object
# @parameter: 1st parameter - connection object, 2nd parameter - create table statement
# @return: no value
def create_table(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


# Makes a variable that holds the create table statements and calls the create_table function using the conn object
# @parameter: connection object
# @return: no value
def initialize_table(conn):
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS Log (
                                        timeOfInsert varchar(64) PRIMARY KEY,
                                        fileName varchar(128),
                                        timestamp varchar(128),
                                        permissions varchar(128),
                                        isNewFile boolean,
                                        hash varchar default false
                                    ); """
    # create a database connection
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

    else:
        print("Error! cannot create the database connection.")


# Inserts a row in the database based on the parameters passed
# @parameter: 1 - connection object, 2 - time of insertion in database, 3 - name of file,
#             4 - time stamp when file was last modified, 5 - permissions of file, 6 - hash value
# @return: no values
def insert_column(conn, time_of_insert, filename, timestamp, permissions, hashed):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Log VALUES (?, ?, ?, ?, ?, ?);",
                   (time_of_insert, filename, timestamp, permissions, True, hashed))
    conn.commit()


# Select everything from the Log table where the file was most recently added
# @parameter: connection object
# @return: results from the select query in a list of tuples
def select_columns(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Log WHERE isNewFile=1")
    results = cursor.fetchall()
    return results


# Update the database to set all old data's isNewFile column to false so we can identify the new data that was inserted
# @parameter: connection object
# @return: no values
def set_everything_to_false(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE Log SET isNewFile = 0")


# Insert a batch of data by passing a list of file objects as a parameter to the function. It iterates through the
# list and inserts each record in the database
# @parameter: 1 - connection object, 2 - list of file objects which has data like name, timestamp etc
# @return: no value
def batch_insert(conn, current_files):
    # if len(current_files) == 0:
    #     set_everything_to_false(conn)
    #     conn.commit()
    # else:
    for files in current_files:
        cur_file = current_files[files]
        current_time = time.time()
        file_name = cur_file.name
        time_stamp = cur_file.timestamp
        permissions = str(cur_file.permissions)
        file_hash = str(cur_file.file_hash)
        insert_column(conn, current_time, file_name, time_stamp, permissions, file_hash)


# This function queries the whole table and fetches all the historic data about the files
# @parameter: connection object
# @return: all results
def get_historic_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Log;")
    results = cursor.fetchall()
    # print(results[0])
    return results


def main():
    conn = create_connection("test2.db")
    initialize_table(conn)

    # insert_column(conn, "1:29", "filename.txt", "3:45", "777", "gaurav")
    # insert_column(conn,"1:49", "filename.txt", "3:45", "777", "gaurav")

    # results = select_columns(conn)
    # print(results)

    conn.close()


if __name__ == '__main__':
    main()
