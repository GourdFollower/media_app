import mysql
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name, user = user_name, passwd = user_password, database = db_name
        )
        print("Connection to MySQL exists")
    except Error as e:
        print(f"You are disconnected due to error '{e}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query has been queried")
    except Error as e:
        print(f"Query remains unqueried due to error '{e}'")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Query remains unqueried due to error '{e}'")


def insert_query(connection):
    sql = "insert into users (id, username, password) values (%s, %s, %s)"
    val = [(1, "Chihiro", "1234"), (2, "Kiki", "5678")]

    cursor = connection.cursor()
    cursor.executemany(sql, val)
    connection.commit()

create_users_table = """create table if not exists users (
id int, username text not null, password text not null);"""

connection = create_connection("localhost", "root", "C4nticl3?", "menagerie")
# password probably *shouldn't* be hardcoded into the file, but what can you do?

select_users = "select * from users"
users = execute_read_query(connection, select_users)
for user in users:
    print(user)
