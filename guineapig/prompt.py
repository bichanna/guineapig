from cmd import Cmd
import mysql.connector
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
	
	def do_list(self, inp):
		"""Show the all items stored in database"""
		connection, cursor = utils.connect_db()
		with connection:
			cursor.execute("SELECT * FROM item")
			result = cursor.fetchall()
			if len(result) == 0:
				print("There are no items. Create one with 'create item'")
			for row in result:
				print(row)
				print("\n")
			cursor.close()


	def do_create(self, inp):
		"""'create category' or 'create item'"""
		cnx = mysql.connector.connect(user="root",database="guineapig_db")
		cursor = cnx.cursor()
		with cnx:
			if inp == "category":
				category_name = input("   category name: ")
				try:
					command = "INSERT INTO category (category_name) VALUES ('{}')".format(category_name)
					cursor.execute(command)
					cnx.commit()
				except:
					utils.guineapig_print("Error occured. Please try again.")
				cursor.close()

			elif inp == "item":
				try:
					value = float(input("   item value: "))
					memo = input("   memo(optional): ")
					try:
						cursor.execute(f"INSERT INTO item (item_value, memo) VALUES ('{value}', '{memo}')")
						cursor.execute(command)
						cnx.commit()
					except:
						utils.guineapig_print("Error occured. Please try again.")
				except ValueError:
					utils.guineapig_print("Invalid input")
			else:
				utils.guineapig_print("Invalid command. 'create category' or 'create item'")

		











