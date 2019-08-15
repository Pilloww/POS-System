import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
# import global_var
def dbdr(self):
  try:
     conn = mysql.connector.connect(host='localhost',
                                  database='test1',
                                  user='',                #input username between quotations
                                  password='')            #input password between quotations
     cursor = conn.cursor()

     #return data stored in tables
     setup_query = """SELECT * FROM Setup """
     
     cursor.execute(setup_query)
     global location
     location = cursor.fetchall()
     global current_table
     current_table = cursor.rowcount

  except mysql.connector.Error as error :
    print("Failed to retrieve table{}".format(error))
  finally:
    #closing database connection
    if(conn.is_connected()) :
      cursor.close()
      conn.close()
      print("connection is closed")
      