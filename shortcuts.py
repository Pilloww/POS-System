#global variables
import tkinter as tk
from database_accessor import ts_insert
import db_data_return as dbdr
global object_list
object_list = []
#Info is super/parent class
class Info :
#a list with 2 empty lists called entry_input is created
#the first list entry_input[0] will contain name/description of the data stored in coresponding index in the second list: entry_input[1]   
	def __init__(self, table_id):
		self.table_id = table_id
		self.entry_input = [[],[]]
#as this list is a temporary object for clarity when debegging, it may be removed
	def table_setup(self):
		self.entry_input[0].append('Name')
		self.entry_input[0].append('Id')
		self.entry_input[0].append('Split')
		self.entry_input[0].append('Shape')
		self.entry_input[0].append('x1')
		self.entry_input[0].append('y1')
		self.entry_input[0].append('x2')
		self.entry_input[0].append('y2')
		self.entry_input[0].append('Occupancy')
		self.entry_input[0].append('Max_Seating')
		self.entry_input[0].append('Current_Seated')
#prints temporary object for debegging purposes - may be removed
	def details(self):
		print(self.entry_input)

class table_setup(Info):
	def __init__(self, table_id):
		super().__init__(table_id)
		self.table_setup()
#an entry class to simplify entry creation
#user_input() - retrieves data from entries
#entry_create() - creates empty entries
#entry_update() - creates entries with values from database for updating
#obj_name is the given name(string) of the object that will be stored in the list

class Entries:
	def user_input(self, entry_size, action):	
			object_name = object_list[action]
			ts_insert(object_name.entry_input[1][0].get(), object_name.entry_input[1][1].get(), object_name.entry_input[1][2].get(), object_name.entry_input[1][3].get(), object_name.entry_input[1][4].get(), object_name.entry_input[1][5].get(), object_name.entry_input[1][6].get(), object_name.entry_input[1][7].get(), object_name.entry_input[1][8].get(), object_name.entry_input[1][9].get())
				
	def entry_create(self, size, frame, relwidth, relheight, relx, rely, increment, obj_name):
			global object_name
			object_name = obj_name
			object_name = table_setup(None)
			counter = 0
			while counter < size:
				object_name.entry_input[1].append(tk.Entry(frame, font=30))
				object_name.entry_input[1][counter].place(relx = relx, rely = rely, relwidth = relwidth,
					 relheight = relheight)		  
				counter += 1
				relx += increment
			object_list.append(object_name)
	def entry_update(self, size, frame, relwidth, relheight, relx, rely, increment, obj_name, index):
			self.object_name = obj_name
			self.object_name = table_setup(None)
			tuple_counter = (1,2,8,9,10) # indexes in database of which elements to be updated are stored
			counter = 0
			self.index = int(index)		# -1 because Name starts at 1 but index starts at 0	
			while counter < size:
				self.object_name.entry_input[1].append(tk.Entry(frame, font=30))
				self.object_name.entry_input[1][counter].place(relx = relx, rely = rely, relwidth = relwidth,
					 relheight = relheight)
				self.object_name.entry_input[1][counter].insert(0, '{}'.format(dbdr.location[self.index][tuple_counter[counter]]))
				counter += 1
				relx += increment
			object_list.append(self.object_name)			
#a class that calls and returns data currently within the database
#db_t_setup() will call all rows in the database and return as string
#db_setup_coords() will call specific columns (x1,y1,x2,y2,shape,name) of every row and append them to a list of lists
class db_caller :
	def db_t_setup(self):
		global data_hold1
		data_hold1 = []
		dbdr.dbdr(1)
		for dbdr.row in dbdr.location:
		 data_hold1.append('{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(dbdr.row[0], dbdr.row[1], dbdr.row[2], dbdr.row[3], dbdr.row[4], dbdr.row[5], dbdr.row[6], dbdr.row[7], dbdr.row[8], dbdr.row[9], dbdr.row[10]))
		s1string = 'Amount of table types: {}\n'.format(dbdr.current_table)
		s2string = 'Table Setup:\n'
		counter = 0
		s3string = ''
		while(counter<len(data_hold1)):
			s3string += '{}\n'.format(data_hold1[counter])
			counter += 1
		return s1string + s2string + s3string
	def db_setup_coords(self):
		global data_hold2
		data_hold2 = [[],[],[],[],[],[]]
		dbdr.dbdr(1)
		for dbdr.row in dbdr.location:
		 data_hold2[0].append(dbdr.row[4]) #x1
		 data_hold2[1].append(dbdr.row[5]) #y1
		 data_hold2[2].append(dbdr.row[6]) #x2
		 data_hold2[3].append(dbdr.row[7]) #y2
		 data_hold2[4].append(dbdr.row[3]) #shape
		 data_hold2[5].append(dbdr.row[0]) #name
		return data_hold2