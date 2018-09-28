import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

def create_table(connection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param connection: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


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


def insert_column(conn, timeofinsert, filename, timestamp, permissions, hashed):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Log VALUES (?, ?, ?, ?, ?, ?);",(timeofinsert, filename, timestamp, permissions, True, hashed))


def select_columns(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Log WHERE isNewFile=1")
    results = cursor.fetchall()
    return results


def set_everything_to_false(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE TABLE SET isNewFile = False")


def main():
    conn = create_connection("test.db")
    initialize_table(conn)
    insert_column(conn, "1:08", "filename.txt", "3:45", "777", "gaurav")

    results = select_columns(conn)
    print(results)

if __name__ == '__main__':
    main()

