import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        return None
    finally:
        return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def drop_table(conn, drop_table_sql):
    """ drop a table from the drop_table_sql statement
        :param conn: Connection object
        :param drop_table_sql: a DROP TABLE statement
        :return:
        """
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
    except Error as e:
        print(e)


def create_result(conn, result):
    """
    Create a new project into the projects table
    :param conn:
    :param result:
    :return: project id
    """
    sql = ''' INSERT INTO results(url,title) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, result)
    rowid = cur.lastrowid
    return rowid

def search_result(conn, url):
    """
        Create a new project into the projects table
        :param conn:
        :param url:
        :return: project id
        """
    sql = ''' SELECT * FROM results WHERE url= \"'''
    cur = conn.cursor()
    cur.execute(sql + url + "\"")
    return cur.fetchone()


if __name__ == '__main__':
    conn = create_connection("pythonsqlite.db")
    #resets the table if you want to be able to see old results
    drop_table(conn, "DROP TABLE IF EXISTS results")
    create_table(conn, "CREATE TABLE IF NOT EXISTS results (url text PRIMARY KEY, title text NOT NULL)")
    create_result(conn, ('test', 'test'))
    curr = conn.cursor()
    curr.execute("SELECT * FROM results")
    entries = curr.fetchall();
    if entries is None:
        pass
    else:
        print(entries)

