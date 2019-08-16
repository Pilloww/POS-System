import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from inputs import inputs
#function that inserts newly drawn tables into database
def ts_insert(Id, Split, Shape, x1, y1, x2, y2, Occupancy, Max_Seating, Current_Seated):
  user_data = inputs()
  try:
     conn = mysql.connector.connect(host=user_data.Host,
                               database=user_data.Database,
                               user=user_data.Username,      #input username between quotations
                               password=user_data.Password)  #input password between quotations 
     cursor = conn.cursor()

#Insertion
     sql_insert_query = """INSERT INTO Setup(Id, Split, Shape, x1, y1, x2, y2, Occupancy, Max_Seating, Current_Seated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

     input = (Id, Split, Shape, x1, y1, x2, y2, Occupancy, Max_Seating, Current_Seated)
     cursor.execute(sql_insert_query, input)
     conn.commit()
     print("Table setup inserted successfully")

  except mysql.connector.Error as error :
     conn.rollback()
     print("Failed to insert Table Setup into MySQL table\n {}". format(error))
  finally:
  	#closing database connection
  	if(conn.is_connected()) :
  		cursor.close()
  		conn.close()
  		print("Connection is Closed")
#function that updates the table data in database
def ts_update(x1, y1, x2, y2, Id, Split, Occupancy, Max_Seating, Current_Seated):
  user_data = inputs()
  try:
     conn = mysql.connector.connect(host=user_data.Host,
                               database=user_data.Database,
                               user=user_data.Username,           #input username between quotations
                               password=user_data.Password)       #input password between quotations
     cursor = conn.cursor()

#Update 
     sql_update_query = """UPDATE Setup SET Id = %s, Split = %s, Occupancy = %s, Max_Seating = %s, 
     Current_Seated = %s WHERE x1 = %s and y1 = %s and x2 = %s and y2 = %s"""

     if(Id == 'None'):
      Id = None
     if(Max_Seating == 'None'):
      Max_Seating = None
     if(Current_Seated == 'None'):
      Current_Seated = None
     input = (Id, Split, Occupancy, Max_Seating, Current_Seated, int(x1), int(y1), int(x2), int(y2))
     cursor.execute(sql_update_query, input)
     conn.commit()
     print ("Record updated successfully ")
  except mysql.connector.Error as error :
      print("Failed to update record to database: {}".format(error))
  finally:
      #closing database connection.
      if(conn.is_connected()):
          conn.close()
          print("Connection is Closed")
#function that updates table location
def move_update(x1, y1, x2, y2, Name):
  user_data = inputs()
  try:
     conn = mysql.connector.connect(host=user_data.Host,
                               database=user_data.Database,
                               user=user_data.Username,                 #input username between quotations
                               password=user_data.Password)             #input password between quotations
     cursor = conn.cursor()

#Update 
     sql_update_query = """UPDATE Setup SET x1 = %s, y1 = %s, x2 = %s, y2 = %s 
     WHERE Name = %s"""
     input = (int(x1), int(y1), int(x2), int(y2), Name)
     cursor.execute(sql_update_query, input)
     conn.commit()
     print ("Record updated successfully ")
  except mysql.connector.Error as error :
      print("Failed to update record to database: {}".format(error))
  finally:
      #closing database connection.
      if(conn.is_connected()):
          conn.close()
          print("Connection is Closed")
#function that deletes table from database
def ts_delete(self, x1, y1, x2, y2):
  user_data = inputs()
  try:
     conn = mysql.connector.connect(host=user_data.Host,
                               database=user_data.Database,
                               user=user_data.Username,                 #input username between quotations
                               password=user_data.Password)             #input password between quotations
     cursor = conn.cursor()

#Deletion
     sql_Delete_query = """DELETE FROM Setup where x1 = %s and y1 = %s and x2 = %s and y2 = %s""" 
     input = (x1, y1, x2, y2)
     cursor.execute(sql_Delete_query, input)
     conn.commit()
     print("\nRecord deleted successfully ")

  except mysql.connector.Error as error :
    print("Failed to delete record: {}".format(error))
  finally:
    #closing database connection
    if(conn.is_connected()) :
      cursor.close()
      conn.close()
      print("Connection is Closed")