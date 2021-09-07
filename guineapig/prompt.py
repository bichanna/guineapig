from cmd import Cmd
import mysql.connector
try:
	import utils
except:
	from . import utils


list_print = """ - ${}
 - MEMO: {}
 - DATE: {}
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
	
	def do_list(self, inp):
		"""Show the all items stored in database"""
		connection, cursor = utils.connect_db()
		with connection:
			cursor.execute("SELECT * FROM item")
			result = cursor.fetchall()
			if len(result) == 0:
				print("There are no items. Create one with 'create item'")
			else:
				print("items")
				for row in result:
					category_id = row[2]
					print(list_print.format(row[1], row[3], row[4]))
			cursor.close()


	def do_create(self, inp):
		"""'create category' or 'create item'"""
		cnx = mysql.connector.connect(user="root",database="guineapig_db")
		cursor = cnx.cursor()
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

		











