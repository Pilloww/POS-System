import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from inputs import inputs
# import global_var
def dbdr(self):
  user_data = inputs()
  try:
     conn = mysql.connector.connect(host=user_data.Host,
                                  database=user_data.Database,
                                  user=user_data.Username,                #input username between quotations
                                  password=user_data.Password)            #input password between quotations
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
      