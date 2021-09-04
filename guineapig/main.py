import click
from prompt import Prompt
import subprocess
import mysql.connector
from mysql.connector.errors import DatabaseError
import sys
import platform

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
			print("GUINEAPIG: Start installing mysql")
			output = subprocess.check_output(["brew", "install", "mysql"]).decode("utf-8")
			if "brew services restart mysql" in output:
				print("mysql is installed.")
		except FileNotFoundError:
			homebrew_url = "https://brew.sh/"
			print(f"homebrew is not installed. Please install homebrew: {homebrew_url}").decode("utf-8")
			sys.exit()

	# create database if it does not exit
	db = mysql.connector.connect(user="root")
	cursor = db.cursor()
	try:
		cursor.execute("CREATE DATABASE guineapig_db")
		print("GUINEAPIG: Database `guineapig_db` is created.")
	except DatabaseError:
		print("GUINEAPIG: Database `guineapig_db` already exits.")



@main.command()
def shell():
	cnx = mysql.connector.connect(user="root",database="")
	Prompt().cmdloop()


if __name__ == "__main__":
	if platform.system() != "Darwin":
		print("guineapig is currently only for Mac users.")
		sys.exit()
	main()






