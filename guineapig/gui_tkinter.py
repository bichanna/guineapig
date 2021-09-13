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
				self.text = Text(root, width=15, fg='white', height=3)
				self.text.grid(row=i, column=j+10)
				if result[i][j] is not None:
					self.text.insert(END, result[i][j])
				else:
					self.text.insert(END, "None")
				self.text.configure(state="disabled")

def get_all():
	connection, cursor = utils.connect_db()
	with connection:
		root = Tk()
		root.title("guineapig GUI")
		root.geometry("650x650")
		cursor.execute("SELECT * FROM item ORDER BY item_id DESC")
		result = cursor.fetchall()
		if len(result) == 0:
			label = Label(text="There are no items. Create one.")
		else:
			table = Table(root, result)
			root.mainloop()
