import tkinter as tk
from shortcuts import *
from database_accessor import *
import db_data_return as dbdr
from PIL import ImageTk
from math import sqrt
import time
#stores data from database into a variable 'coords'
global coords
coords = db_caller().db_setup_coords()
#Page class is the parent class
class Page(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.coords = coords
		self.counter = 0
#creates canvas which holds the image and shapes
	def create_canvas(self):
		self.canvas = tk.Canvas(self, bg = '#7FA6D9')
		self.canvas.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)
#*****************************add file directory to background image below
		self.layout = ImageTk.PhotoImage(file = '') #insert between quotations
		self.image = self.canvas.create_image(100, 0, anchor='n', image=self.layout, state='disabled')
#creates the label at the top of the page
	def create_page_label(self, name): 
		self.label = tk.Label(self, bg='#7FA6D9', text= name, anchor='n', font=40)
		self.label.pack(side='top', fill='both', expand=True)
#lifts page to the surface and updates it
	def show(self):
		self.canvas_refresh()
		self.lift()
#updates shapes on canvas - pulls data from database and redraws shapes
	def refresh(self):
			self.coords = db_caller().db_setup_coords()
			self.counter = 0
			while (self.counter < len(self.coords[0])):
				if(self.coords[4][self.counter] == 'Circle'):
					self.stuff = '{}'.format(self.coords[5][self.counter])
					self.stuff = self.canvas.create_oval(self.coords[0][self.counter], self.coords[1][self.counter], self.coords[2][self.counter], self.coords[3][self.counter], fill='violet', width=2, activefill='orange', tags=(self.stuff, 'Circle', self.counter))
					self.text = self.canvas.create_text(((self.coords[2][self.counter]-self.coords[0][self.counter])/2+self.coords[0][self.counter]), ((self.coords[3][self.counter]-self.coords[1][self.counter])/2+self.coords[1][self.counter]), text = self.coords[5][self.counter], font=15, tags=(self.stuff, 'Circle'), state='disabled' )
				elif(self.coords[4][self.counter] == 'Rectangle'):
					self.stuff = '{}'.format(self.coords[5][self.counter])
					self.stuff = self.canvas.create_rectangle(self.coords[0][self.counter], self.coords[1][self.counter], self.coords[2][self.counter], self.coords[3][self.counter], fill='violet', width=2, activefill='orange', tags=(self.stuff, 'Rectangle', self.counter))
					self.text = self.canvas.create_text(((self.coords[2][self.counter]-self.coords[0][self.counter])/2+self.coords[0][self.counter]), ((self.coords[3][self.counter]-self.coords[1][self.counter])/2+self.coords[1][self.counter]), text = self.coords[5][self.counter], font=15, tags=(self.stuff, 'Rectangle'), state='disabled' )
				self.counter += 1
#clears canvas and redraws
	def canvas_refresh(self):
		self.canvas.delete('all')
#****************************add file directory to background image below
		self.layout = ImageTk.PhotoImage(file = '') #insert between quotations
		self.image = self.canvas.create_image(100, 0, anchor='n', image=self.layout, state='disabled')			
		self.refresh()
#Child classes 
#___________________________________________________________________________________________________________
#Note: lambda function is used in button commands to prevent function attached to button from running on application startup
#displays data currently stored in database
class DatabasePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Database')

#frame - db output
		frame = tk.Frame(self, bg='gray', bd=5)
		frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

		self.label_left = tk.Label(frame, bg='#6383c9', anchor='n')
		self.label_left.place(relwidth=1, relheight=1)
		self.label_left['text'] = db_caller().db_t_setup()
#functions as its unique lift function 
	def reveal(self):
		self.label_left['text'] = db_caller().db_t_setup()
		self.lift()
#opens new window to insert table information on mouse click
class UpdatePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Update')
		self.create_canvas()
		self.refresh()
		self.canvas.bind("<Button-1>", self.table_selected)
#creates new window based on table clicked - opened window takes user inputs for entries
	def table_selected(self, event):
		(self.x1, self.y1, self.x2, self.y2) = self.canvas.coords(event.widget.find_withtag("current"))
		(table_name, self.shape_selected, index, garbage) = self.canvas.gettags(event.widget.find_withtag("current"))
		window = tk.Tk()			#creates the new window
		window.title('Updating Information for Table {}'.format(table_name))  #title of the window
		window.geometry('800x250-5+40')
		frame = tk.Frame(window, bg='#7FA6D9')
		frame.place(relx=0, rely=0, relwidth=1, relheight=1)
		label_tuple = ('Id', 'Split', 'Occupied', 'Max', 'Current')
		for i in range(5):
			increment = i*0.15
			labels = tk.Label(frame, bg='#7FA6D9', text=label_tuple[i], font=20)
			labels.place(relx=0.145+increment, rely=0.2, relwidth=0.1, relheight=0.1)
		update_entries = Entries()
		update_entries.entry_update(5, frame, 0.1, 0.1, 0.15, 0.45, 0.15, 'updater', index)
#update() uploads inputted data to database then closes window
		def update(self):
			ts_update(self.x1, self.y1, self.x2, self.y2, update_entries.object_name.entry_input[1][0].get(), update_entries.object_name.entry_input[1][1].get(),update_entries.object_name.entry_input[1][2].get(), update_entries.object_name.entry_input[1][3].get(), update_entries.object_name.entry_input[1][4].get())
			window.destroy()
			self.canvas_refresh()
#cancel() closes window
		def cancel(self):
			window.destroy()
		update_button = tk.Button(frame, bg='#669ce8', text='Update', font=20, command = lambda: update(self))
		update_button.place(relx= 0.3, rely=0.7, relwidth=0.2, relheight=0.2)
		cancel_button = tk.Button(frame, bg='#669ce8', text='Cancel', font=20, command = lambda: cancel(self))
		cancel_button.place(relx= 0.5, rely=0.7, relwidth=0.2, relheight=0.2)
		window.mainloop()			#end of window definitions
#moves table on mouseclick and drag
class MovePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Move')
		self.create_canvas()
		self.refresh()
		self.canvas.bind('<B1-Motion>', self.move_shape)
		self.canvas.bind('<Button-1>', self.click)
		self.canvas.bind('<ButtonRelease-1>', self.release)
#determines table clicked and stores intial table coords
	def click(self, event):
			self.current = event.widget.find_withtag("current")
			(self.table_name, *garbage) = self.canvas.gettags(event.widget.find_withtag("current"))
			(self.x1, self.y1, self.x2, self.y2) = self.canvas.coords(event.widget.find_withtag("current"))
#moves table to current mouse position while holding down mouse click
	def move_shape(self, event):
			size_x = (self.x2 - self.x1)/2
			size_y = (self.y2 - self.y1)/2
			self.new_x1 = event.x-size_x
			self.new_y1 = event.y-size_y
			self.new_x2 = event.x+size_x
			self.new_y2 = event.y+size_y
			self.canvas.coords(self.current, self.new_x1, self.new_y1, self.new_x2, self.new_y2)
#uploads new coords to database and refreshes canvas to prevent duplication
	def release(self, event):
			move_update(self.new_x1, self.new_y1, self.new_x2, self.new_y2, int(self.table_name))
			self.canvas_refresh()
#Resizes tables by clicking and dragging
class ResizePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Resize')
		self.create_canvas()
		self.refresh()
		self.canvas.bind('<B1-Motion>', self.move_shape)
		self.canvas.bind('<Button-1>', self.click)
		self.canvas.bind('<ButtonRelease-1>', self.release)
#determines table clicked and stores its coords
	def click(self, event):
			self.current = event.widget.find_withtag("current")
			(self.table_name, *garbage) = self.canvas.gettags(event.widget.find_withtag("current"))
			(self.x1, self.y1, self.x2, self.y2) = self.canvas.coords(event.widget.find_withtag("current"))
			self.event_x = event.x
			self.event_y = event.y
#increases or decreases size of table on mouse hold and drag
	def move_shape(self, event):
			distance = sqrt(pow((event.x-self.event_x), 2) + pow((event.y-self.event_y), 2))
			if (event.x-self.event_x <= 0 or event.y-self.event_y <= 0):
				self.new_x1 = self.x1+distance
				self.new_y1 = self.y1+distance
				self.new_x2 = self.x2-distance
				self.new_y2 = self.y2-distance
			else:
				self.new_x1 = self.x1-distance
				self.new_y1 = self.y1-distance
				self.new_x2 = self.x2+distance
				self.new_y2 = self.y2+distance
			self.canvas.coords(self.current, self.new_x1, self.new_y1, self.new_x2, self.new_y2)
#stores new size coords to database and refreshes canvas to prevent duplication
	def release(self, event):
			move_update(self.new_x1, self.new_y1, self.new_x2, self.new_y2, int(self.table_name))
			self.canvas_refresh()
#selects table on mouseclick and deletes from database when 'Confirm' is clicked
class DeletePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Delete')
		self.create_canvas()
		self.delete_button_frame = tk.Frame(self)
		self.delete_button_frame.pack(side='bottom', fill='x', expand=False)
#deletes table from database then refreshes
		def deleted(self):
			ts_delete(self, self.x1, self.y1, self.x2, self.y2)
			self.canvas_refresh()
		self.delete_button = tk.Button(self.delete_button_frame, bg='gray', text='Confirm', font=20, command= lambda: deleted(self)) 
		self.delete_button.pack()
		self.refresh()
		self.canvas.bind("<Button-1>", self.table_selected)
		self.check = False
#identifies and highlights which table is selected
	def table_selected(self, event):
		(self.x1, self.y1, self.x2, self.y2) = self.canvas.coords(event.widget.find_withtag("current"))
		self.canvas.itemconfig(event.widget.find_withtag("current"), fill='orange')
		self.current = event.widget.find_withtag("current")
		if (self.check == True):
			self.canvas.itemconfig(self.previous, fill='violet')
			self.previous = event.widget.find_withtag("current")
		else: 
			self.previous = event.widget.find_withtag("current")
			self.check = True
#draws new tables on mouse click and drag -> 'Save' button adds it to the database
class DrawPage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Draw')
		self.checkFrame = tk.Frame(self, bg='gray')
		self.checkFrame.pack(side='bottom')
		self.x = 0
		self.y = 0
		self.shape = None
		self.circle_var= tk.IntVar()
		self.rectangle_var = tk.IntVar()
		self.shape_store = None
#deselects the circle checkbox and stores data for rectangle creation
		def deselect_circle(self):		
			self.check_circle.deselect()
			self.shape = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill='violet', width=2)
			self.shape_store = 'Rectangle'
#deselects the rectangle checkbox and stores data for circle creation
		def deselect_rectangle(self):
			self.check_rectangle.deselect()
			self.shape = self.canvas.create_oval(self.x, self.y, 1 , 1, fill='violet', width=2)
			self.shape_store = 'Circle'
#stores newly created shape data into database
		def save_coords(self):
			ts_insert(None, 'No', self.shape_store, start_store[0], start_store[1], end_store[0], end_store[1], 'No', None, None)
			self.counter = len(self.coords[5])
			self.coords[0].append(start_store[0])
			self.coords[1].append(start_store[1])
			self.coords[2].append(end_store[0])
			self.coords[3].append(end_store[1])
			self.coords[4].append(self.shape_store)
			self.new_name = self.coords[5][self.counter-1] +1
			self.coords[5].append(self.new_name)
			if (self.shape_store == 'Circle'):
				self.new_add = 'self.shape_object{}'.format(self.new_name)
				self.new_add = self.canvas.create_oval(start_store[0], start_store[1], end_store[0], end_store[1], fill='violet', width=2)
				self.text = self.canvas.create_text(((end_store[0]-start_store[0])/2+start_store[0]), ((end_store[1]-start_store[1])/2+start_store[1]), text = self.coords[5][self.counter], font=15, tags=self.new_add )
			if (self.shape_store == 'Rectangle'):
				self.new_add = 'self.shape_object{}'.format(self.new_name)
				self.new_add = self.canvas.create_rectangle(start_store[0], start_store[1], end_store[0], end_store[1], fill='violet', width=2)			
				self.text = self.canvas.create_text(((end_store[0]-start_store[0])/2+start_store[0]), ((end_store[1]-start_store[1])/2+start_store[1]), text = self.coords[5][self.counter], font=15, tags=self.new_add )
		self.check_circle = tk.Checkbutton(self.checkFrame, bg='gray', text='Circle', font=20, variable=self.circle_var, onvalue=1, offvalue=0,height=1, width=20, command= lambda: deselect_rectangle(self))
		self.check_rectangle = tk.Checkbutton(self.checkFrame, bg='gray', text='Rectangle', font=20, variable=self.rectangle_var, onvalue=1, offvalue=0,height=1, width=20, command= lambda: deselect_circle(self))
		self.save_button = tk.Button(self.checkFrame, bg='gray', text='Save', font=20, command= lambda : save_coords(self))
		self.check_circle.pack(side='left')
		self.check_rectangle.pack(side='left')
		self.save_button.pack(side='left')
		self.create_canvas()
		self.canvas.bind("<Button-1>", self.click)
		self.canvas.bind("<ButtonRelease-1>", self.release)
		self.canvas.bind("<B1-Motion>", self.move)
		self.canvas_refresh()
		self.type = None
		self.start_x = None
		self.start_y = None
#determines coords of initial click
	def click(self, event):
		self.start_x = event.x
		self.start_y = event.y
		self.type = self.shape
		global start_store
		start_store = []
		start_store.append(event.x)
		start_store.append(event.y)
	def release(self, event):
		pass
#determines coords of current mouse position while holding down and alters shape size
	def move(self, event):
		x_current = event.x
		y_current = event.y
		self.canvas.coords(self.shape, self.start_x, self.start_y, x_current, y_current)
		global end_store
		end_store = []
		end_store.append(event.x)
		end_store.append(event.y)
#unique lift function to invoke circle checkbox
	def show(self): 
		super(DrawPage, self).show()
		self.check_circle.invoke()
#displays the current setup
class DisplayPage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.create_page_label('Display')
		self.create_canvas()
#automatic refresh after x time - can be removed
		def refresh(): #adds timer for an automatic refresh
			super(DisplayPage, self).refresh()
			self.canvas.after(120000, refresh)
		refresh()
#end of Child classes_______________________________________________________________________________________

#page viewer - initializes all the pages and buttons to navigate between pages
class View(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs) 
		self.Database = DatabasePage(self)
		self.Update = UpdatePage(self)
		self.Move = MovePage(self)
		self.Resize = ResizePage(self)
		self.Delete = DeletePage(self)
		self.Draw = DrawPage(self)
		self.Display = DisplayPage(self)

		self.buttonframe = tk.Frame(self)
		self.container = tk.Frame(self)
		self.buttonframe.pack(side='bottom', fill='x', expand=False)
		self.container.pack(side='bottom', fill='both', expand=True)

		self.Database.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
		self.Update.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
		self.Move.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
		self.Resize.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
		self.Delete.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
		self.Draw.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
		self.Display.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

		self.Database_button = tk.Button(self.buttonframe, text='Database', font=25, command=self.Database.reveal)
		self.Database_button.pack(side='left')
		self.update_button = tk.Button(self.buttonframe, text='Update', font=25, command=self.Update.show)
		self.update_button.pack(side='left')
		self.move_button = tk.Button(self.buttonframe, text='Move', font=25, command=self.Move.show)
		self.move_button.pack(side='left')
		self.resize_button = tk.Button(self.buttonframe, text='Resize', font=25, command=self.Resize.show)
		self.resize_button.pack(side='left')		
		self.delete_button = tk.Button(self.buttonframe, text='Delete', font=25, command=self.Delete.show)
		self.delete_button.pack(side='left')
		self.draw_button = tk.Button(self.buttonframe, text='Draw', font=25, command=self.Draw.show)
		self.draw_button.pack(side='left')
		self.display_button = tk.Button(self.buttonframe, text='Display', font=25, command=self.Display.show)
		self.display_button.pack(side='left')

		self.Database.lift()
#calls the page initializer (View) and runs the program
if (__name__ == '__main__'):

	root = tk.Tk()
	main = View(root)
	main.pack(side='top', fill='both', expand=True)
	root.wm_geometry("900x700")
	root.mainloop()
