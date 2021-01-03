import mysql.connector

import mysql.connector

'''connecting to local database'''
database = mysql.connector.connect(
    host="localhost",
    user="user",
    password="123",
    database="wypozyczalnia_kostiumow"
)

# print(database)

cursor = database.cursor()

# my_cursor.execute("SHOW TABLES")
# for x in my_cursor:
#   print(x)

cursor.execute("SELECT * FROM klient")
clients = cursor.fetchall()
for client in clients:
    print(client)
