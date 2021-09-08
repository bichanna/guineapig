from cmd import Cmd
import mysql.connector
import datetime
try:
	import utils
except:
	from . import utils


list_print = """
ID : {}
 - DATE: {}
 - ${}
 - MEMO: {}
 -----------------
"""



class Prompt(Cmd):
	prompt = "guineapig>> "
	intro = "GUINEAPIG🐹"

	# exit 
	def do_exit(self, inp):
		"""Exit from shell"""
		print("Bye")
		return True

	do_EOF = do_exit

	do_quit = do_exit

	def do_show(self, inp):
		"""List items created in particular month or year"""
		inputs = inp.split(" ")
		try:
			value1 = int(inputs[-1])
		except:
			utils.guineapig_print("Invalid input")

		if len(inputs) >= 2:
			today = datetime.datetime.today()
			connection, cursor = utils.connect_db()
			with connection:
				if inputs[0] == "month":
					month = value1
					try:
						year = int(inputs[-2])
					except:
						utils.guineapig_print("Invalid input")

					if month >= 1 and month <= 12:
						current_year = today.year
						cursor.execute("SELECT MAX(item_id) FROM item")
						result = cursor.fetchall()
						item_id = result[0][0]
						cursor.execute(f"SELECT * FROM item WHERE item_id = {item_id}")
						result = cursor.fetchall()
						oldest_year = result[0][4].year
						if year <= current_year and year >= oldest_year:
							cursor.execute(f"SELECT * FROM item WHERE MONTH(date_added)={month} AND YEAR(date_added)={year}")
							result = cursor.fetchall()
							if len(result):
								for row in result:
									id = row[0]
									month = row[4].strftime("%B")
									date = f"{month} {row[4].day}, {row[4].year}"
									print(list_print.format(id, date, row[1], row[3]))
							else:
								utils.guineapig_print("No items found.")
						else:
							utils.guineapig_print(f"{oldest_year} ~ {current_year}")
					else:
						utils.guineapig_print("1 ~ 12")

			cursor.close()

		else:
			utils.guineapig_print("Either 'show month <month>', or 'show year <year>'.")
			

	
	def do_listall(self, inp):
		"""Show all items stored in database"""
		connection, cursor = utils.connect_db()
		with connection:
			cursor.execute("SELECT * FROM item")
			result = cursor.fetchall()
			if len(result) == 0:
				print("There are no items. Create one with 'create item'")
			else:
				for row in result:
					category_id = row[2]
					print(list_print.format(category_id, row[4], row[1], row[3]))
			cursor.close()


	def do_create(self, inp):
		"""'create category' or 'create item'"""
		cnx, cursor = utils.connect_db()
		with cnx:
			if inp == "category":
				category_name = input("category name: ")
				try:
					command = "INSERT INTO category (category_name) VALUES ('{}')".format(category_name)
					cursor.execute(command)
					cnx.commit()
				except:
					utils.guineapig_print("Error occured. Please try again.")
				cursor.close()

			elif inp == "item":
				cursor.execute(f"SELECT * FROM category")
				result = cursor.fetchall()
				try:
					value = float(input("item value: "))
					memo = input("memo(optional): ")
					while True:
						category_name = input("category: ")
						if category_name == "abort":
							break
						cursor.execute(f"SELECT category_id FROM category WHERE category_name='{category_name}'")
						result = cursor.fetchall()
						if len(result) == 1:
							category_id = result[0][0]
							try:
								cursor.execute(f"INSERT INTO item (item_value, memo, category_id) VALUES ({value}, '{memo}', {category_id})")
								cnx.commit()
								utils.guineapig_print(f"Saved!")
								break
							except:
								utils.guineapig_print("Error occured. Please try again.")
						else:
							cursor.execute("SELECT * FROM category")
							result = cursor.fetchall()
							if len(result) >= 1:
								print("Categories you can choose from")
								for i in result:
									print(f" - {i[1]}")
							else:
								utils.guineapig_print("There is no category. Create one with 'create category'.")
								break
				except ValueError:
					utils.guineapig_print("Invalid input")
			else:
				utils.guineapig_print("Invalid command. 'create category' or 'create item'")

		











