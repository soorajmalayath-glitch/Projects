import mysql.connector

#creates DB connection
conn= mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sooraj@1607",
    database="testDB"
)

#creates one cursor, to run SQL Queries(Querry runner)
cursor=conn.cursor(dictionary =True)

#Calling cursor.execute() to send our Query to MYSQL
cursor.execute("Select * from users")

#Pulls data from cursor that holds before, for storing python memory 
datas= cursor.fetchall()

for row in datas:
    # if row["id"]>10:

      print(row)


# #Inserting the data into the database
cursor.execute(
   "insert into users (name,age,place) values(%s,%s,%s)",
   ("Athul",24,"London")
)
conn.commit()

#Updating 
cursor.execute(
      "update users set age= %s where id = %s",
      (33,13)
)
conn.commit()
conn.close()
cursor.close()


#deleting 
cursor.execute(
      "delete from users where id = %s",
      (12,)  
)
conn.commit()
conn.close()
cursor.close()

cursor.execute(
      "delete from users where id >= %s",
      (25,)

)

conn.commit()
conn.close()
cursor.close()