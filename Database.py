import sqlite3
from sqlite3 import Error

# create the connection with the database. If there is no db, it creates a new one
# @parameter: path of the database (.db file)
# @return: connection object
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
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
                                        isNewFile boolean varchar(16),
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
def insert_column(conn, timeofinsert, filename, timestamp, permissions, hashed):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Log VALUES (?, ?, ?, ?, ?, ?);",(timeofinsert, filename, timestamp, permissions, True, hashed))
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
    cursor.execute("UPDATE TABLE SET isNewFile = False")


def main():
    conn = create_connection("test.db")
    initialize_table(conn)
    # insert_column(conn, "1:29", "filename.txt", "3:45", "777", "gaurav")
    # insert_column(conn,"1:49", "filename.txt", "3:45", "777", "gaurav")
    results = select_columns(conn)
    print(results)
    conn.close()

if __name__ == '__main__':
    main()

