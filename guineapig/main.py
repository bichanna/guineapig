import click
from prompt import Prompt
import subprocess
import mysql.connector
from mysql.connector.errors import DatabaseError
import sys
import platform
from mysql.connector import errorcode

def guineapig_print(value):
	print(f"GUINEAPIG🐹: {value}")


def check_tables_exist(cnx, table):
	cursor = cnx.cursor()
	cursor.execute("""
		SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = "{}"
	""".format(table))
	if cursor.fetchone()[0] == 1:
		cursor.close()
		return True

	cursor.close()
	return False



@click.group()
def main():
	pass

@main.command()
def setupdb():
	# check if mysql is installed
	try:
		output = subprocess.check_output(["mysql", "--version"]).decode("utf-8")
	except FileNotFoundError:
		# check if homebrew is installed
		try:
			output = subprocess.check_output(["brew", "--version"]).decode("utf-8")
			# install mysql
			guineapig_print("Start installing mysql")
			output = subprocess.check_output(["brew", "install", "mysql"]).decode("utf-8")
			if "brew services restart mysql" in output:
				print("mysql is installed.")
		except FileNotFoundError:
			homebrew_url = "https://brew.sh/"
			print(f"homebrew is not installed. Please install homebrew: {homebrew_url}")
			sys.exit()

	# create database if it does not exist
	cnx = mysql.connector.connect(user="root")
	cursor = cnx.cursor()
	try:
		cursor.execute("CREATE DATABASE guineapig_db")
		guineapig_print("Database `guineapig_db` is created.")
	except DatabaseError:
		guineapig_print("Database `guineapig_db` already exists.")

	# create tables in guineapig_db
	TABLES = {}
	TABLES["category"] = ("""
		CREATE TABLE category (
			category_id CHAR(100),
			category_name VARCHAR(120) NOT NULL,
			PRIMARY KEY (category_id)
		)
	""")
	TABLES["item"] = ("""
		CREATE TABLE item (
			item_id INTEGER,
			item_value DECIMAL(5, 2), # 999.99
			category_id CHAR(100),
			FOREIGN KEY (category_id)
				REFERENCES category(category_id),
			PRIMARY KEY (item_id)
		)
	""")

	cursor.execute("USE guineapig_db")

	for table in TABLES:
		sql = TABLES[table]
		try: 
			cursor.execute(sql)
			guineapig_print(f"Table '{table}' is created.")
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				guineapig_print(f"Table '{table}' exists.")
			else:
				guineapig_print(err.msg)

	cursor.close()
	cnx.close()





@main.command()
def shell():
	# connect to the database if it can be connected
	cnx = None
	try:
		cnx = mysql.connector.connect(user="root",database="guineapig_db")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			guineapig_print("Database `guineapig_db` does not exist.")
			guineapig_print("Please run `guineapig setupdb`.")
			sys.exit()
		elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			guineapig_print("Could not access to `guineapig_db` as root.")
			sys.exit()

	cursor = cnx.cursor()

	# use guineapig_db
	try:
		cursor.execute("USE guineapig_db")
	except mysql.connector.Error as err:
		guineapig_print("Database `guineapig_db` does not exist.")
		guineapig_print("Please run `guineapig setupdb`.")
		sys.exit()

	# check if tables exist
	exist1 = check_tables_exist(cnx, "item")
	exist2 = check_tables_exist(cnx, "category")
	if exist1 and exist2:
		pass
	else:
		guineapig_print("Tables do not exist.")
		guineapig_print("Please run `guineapig setupdb`.")
		sys.exit()

	cursor.close()
	cnx.close()
	Prompt().cmdloop()





if __name__ == "__main__":
	if platform.system() != "Darwin":
		print("guineapig is currently only for Mac users.")
		sys.exit()
	main()






