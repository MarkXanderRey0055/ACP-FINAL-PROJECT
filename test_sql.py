import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="batosai123!",
    database="shipping"
)
print("Connection successful!")
conn.close()
