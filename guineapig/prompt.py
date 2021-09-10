from cmd import Cmd
import mysql.connector
import datetime
import subprocess
import sys
try:
	import utils
except:
	from . import utils




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

	def do_clear(self, inp):
		"""Clear"""
		subprocess.run(["clear"])


	def do_modify(self, inp):
		"""Modify data, specified by ID"""
		try:
			id = int(inp)
		except:
			utils.guineapig_print("Invalid input")
			return
		connection, cursor = utils.connect_db()
		with connection:
			cursor.execute("SELECT * FROM item WHERE item_id={}".format(id))
			result = cursor.fetchall()
			if len(result) == 1:
				id = result[0][0]
				value = result[0][1]
				category_id = result[0][2]
				memo = result[0][3]
				print("Just press enter if you do not want to change")
				while True:
					new_value = input("Amount(${}): ".format(value))
					if new_value == "":
						new_value = value
					try:
						float(new_value)
						break
					except:
						pass
				
				new_memo = input(f"Current memo↓\n{memo}\n: ")
				if new_memo == "":
					new_memo = memo

				cursor.execute("UPDATE item SET item_value={}, memo='{}' WHERE item_id={}".format(new_value, new_memo, id))
				connection.commit()

			elif len(result) == 0:
				utils.guineapig_print("Invalid ID {id}".format)


	def do_list(self, inp):
		"""List items created in particular day, month, or year\n'list day <year> <month> <day>'\n'list month <year> <month>'\n'list year <year>'\n'list all'"""

		connection, cursor = utils.connect_db()
		with connection:
			today = datetime.datetime.today()
			inputs = inp.split(" ")
			# MONTH
			if inputs[0] == "month":
				try:
					month = int(inputs[-1])
				except:
					utils.guineapig_print("Either\n'list day <year> <month> <day>',\n'list month <year> <month>',\n'list year <year>'\n'list all'")
					return
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
						cursor.execute(f"SELECT * FROM item WHERE MONTH(date_added)={month} AND YEAR(date_added)={year} ORDER BY item_id DESC")
						result = cursor.fetchall()
						if len(result) >= 1:
							utils.list_items(result)
						else:
							utils.guineapig_print("No items found.")
					else:
						utils.guineapig_print(f"{oldest_year} ~ {current_year}")
				else:
					utils.guineapig_print("1 ~ 12")

			# YEAR
			elif inputs[0] == "year":
				year = 0
				try:
					year = int(inputs[-1])
				except:
					utils.guineapig_print("Invalid command")
					return
				current_year = today.year
				cursor.execute("SELECT MAX(item_id) FROM item")
				result = cursor.fetchall()
				item_id = result[0][0]
				cursor.execute(f"SELECT * FROM item WHERE item_id = {item_id} ORDER BY item_id DESC")
				result = cursor.fetchall()
				oldest_year = result[0][4].year
				if year <= current_year and year >= oldest_year:
					cursor.execute(f"SELECT * FROM item WHERE YEAR(date_added)={year} ORDER BY item_id DESC")
					result = cursor.fetchall()
					utils.list_items(result)
				else:
					utils.guineapig_print(f"{oldest_year} ~ {current_year}")

			# DAY
			elif inputs[0] == "day":
				try:
					day = int(inputs[-1])
					month = int(inputs[-2])
					year = int(inputs[-3])
				except:
					utils.guineapig_print("Invalid command")
					return
				if day >= 1 and day <= 31:
					if month >= 1 and month <= 12:
						current_year = today.year
						cursor.execute("SELECT MAX(item_id) FROM item")
						result = cursor.fetchall()
						item_id = result[0][0]
						cursor.execute(f"SELECT * FROM item WHERE item_id = {item_id}")
						result = cursor.fetchall()
						oldest_year = result[0][4].year
						if year <= current_year and year >= oldest_year:
							cursor.execute(f"SELECT * FROM item WHERE YEAR(date_added)={year} AND MONTH(date_added)={month} AND DAY(date_added)={day} ORDER BY item_id DESC")
							result = cursor.fetchall()
							if len(result) >= 1:
								utils.list_items(result)
							else:
								utils.guineapig_print("No items found.")
						else:
							utils.guineapig_print(f"{oldest_year} ~ {current_year}")
					else:
						utils.guineapig_print("1 ~ 12")
				else:
					utils.guineapig_print("1 ~ 31")
			# ALL
			elif inputs[0] == "all":
				cursor.execute("SELECT * FROM item ORDER BY item_id DESC")
				result = cursor.fetchall()
				if len(result) == 0:
					print("There are no items. Create one with 'create item'")
				else:
					utils.list_items(result)

		cursor.close()

			

	def do_id(self, inp):
		"""Display the data corresponding to ID\n'id <some id>'"""
		connection, cursor = utils.connect_db()

		try:
			id = int(inp)
		except:
			utils.guineapig_print("Please provide ID.")
			return
		with connection:
			cursor.execute("SELECT * FROM item WHERE item_id={}".format(id))
			result = cursor.fetchall()
			if len(result) == 1:
				utils.list_items(result)
			else:
				utils.guineapig_print("Not found.")


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
					return
				cursor.close()

			elif inp == "item":
				cursor.execute(f"SELECT * FROM category")
				result = cursor.fetchall()
				try:
					value = float(input("amount of money: "))
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

		











