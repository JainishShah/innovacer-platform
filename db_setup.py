import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root"				#your mysql Password
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE db1")
mycursor.execute("use db1")
mycursor.execute("CREATE TABLE user (email VARCHAR(255),series TEXT)")


