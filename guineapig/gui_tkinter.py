from tkinter import *
import mysql.connector
try:
	import utils
except:
	from . import utils


class Table:
	def __init__(self,root, result):
		# code for creating table
		total_rows = len(result)
		total_columns = len(result[0])
		for i in range(total_rows):

			for j in range(total_columns):    
				self.entry = Entry(root, width=40, fg='white')
				self.entry.grid(row=i+1, column=j)
				if result[i][j] is not None:
					self.entry.insert(END, result[i][j])
				else:
					self.entry.insert(END, "None")

def get_all():
	connection, cursor = utils.connect_db()
	with connection:
		root = Tk()
		cursor.execute("SELECT * FROM item ORDER BY item_id DESC")
		result = cursor.fetchall()
		if len(result) == 0:
			label = Label(text="There are no items. Create one.")
		else:
			table = Table(root, result)
			root.mainloop()
