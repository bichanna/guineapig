import click
from .prompt import Prompt
import subprocess
import mysql.connector
from mysql.connector.errors import DatabaseError
import sys
import platform
from mysql.connector import errorcode

def guineapig_print(value):
	print(f"GUINEAPIG🐹: {value}")

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

	# create database if it does not exit
	db = mysql.connector.connect(user="root")
	cursor = db.cursor()
	try:
		cursor.execute("CREATE DATABASE guineapig_db")
		guineapig_print("Database `guineapig_db` is created.")
	except DatabaseError:
		guineapig_print("Database `guineapig_db` already exists.")



@main.command()
def shell():
	# connect to the database if it can be connected
	try:
		cnx = mysql.connector.connect(user="root",database="guineapig_db")
		Prompt().cmdloop()
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_BAD_DB_ERROR:
			guineapig_print("Database `guineapig_db` does not exist.")
			guineapig_print("Please run `guineapig setupdb.`")
			sys.exit()

	# use guineapig_db
	try:
		cursor.execute("USE guineapig_db")
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			guineapig_print("Could not access to `guineapig_db` as root.")
		else:
			guineapig_print("Database `guineapig_db` does not exist.")
			guineapig_print("Please run `guineapig setupdb.`")
		sys.exit()
		




if __name__ == "__main__":
	if platform.system() != "Darwin":
		print("guineapig is currently only for Mac users.")
		sys.exit()
	main()






