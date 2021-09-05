from cmd import Cmd
import mysql.connector

class Prompt(Cmd):
	prompt = "guineapig>> "
	intro = "GUINEAPIG🐹"

	# exit 
	def do_exit(self, inp):
		"""Exit from shell"""
		print("Bye")
		return True

	def do_quit(self, inp):
		"""Exit from shell"""
		return self.do_exit(inp)

	do_EOF = do_exit
	
	def do_list(self, inp):
		"""Show the all items stored in database"""
		cnx = mysql.connector.connect(user="root", database="guineapig_db")
		cursor = cnx.cursor()
		cursor.execute("SELECT * FROM item")
		result = cursor.fetchall()
		if len(result) == 0:
			print("There are no items. Create one with 'create item'")
		for row in result:
			print(row)
			print("\n")


