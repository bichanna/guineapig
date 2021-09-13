from tkinter import *
import mysql.connector
from prettytable import PrettyTable 
try:
	import utils
except:
	from . import utils

class ScrollBar:
	def __init__(self, result, desc):
		root = Tk()
		root.title("guineapig GUI")
		root.geometry("500x300")
		h = Scrollbar(root, orient="horizontal")
		h.pack(side = BOTTOM, fill = X)
		v = Scrollbar(root)
		v.pack(side = RIGHT, fill = Y)
		
		text = Text(root, width=15, height=15, wrap=None, xscrollcommand = h.set, yscrollcommand = v.set)
		columns = []
		for i in desc:
			columns.append(i[0])
		x = PrettyTable(columns)
		for i in result:
			i = list(i)
			id = i[0]
			month = i[4].strftime("%B")
			i[4] = f"{month} {i[4].day}, {i[4].year}"
			x.add_row(i)
		text.insert(END, x)
		text.config(state=DISABLED)
		
		text.pack(side=TOP, fill=X)
		h.config(command=text.xview)
		v.config(command=text.yview)

		root.mainloop()

		



def get_all():
	connection, cursor = utils.connect_db()
	with connection:
		cursor.execute("SELECT * FROM item ORDER BY item_id DESC")
		result = cursor.fetchall()
		if len(result) == 0:
			label = Label(text="There are no items. Create one.")
		else:
			ScrollBar(result, cursor.description)
