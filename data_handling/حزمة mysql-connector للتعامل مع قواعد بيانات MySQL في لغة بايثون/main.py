import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="0000",
    database="sakila",
    port="3306",
)


cursor = db.cursor()

cursor.execute("SELECT first_name, last_name FROM actor WHERE first_name = 'john'")

results = cursor.fetchall()

for result in results:
    print(result)
