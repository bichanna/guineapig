import mysql.connector
import subprocess

list_print = """
ID : {}
 - DATE: {}
 - AMOUNT: \${}
 - MEMO: {}
 -----------------
"""


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


def connect_db():
	cnx = mysql.connector.connect(user="root", database="guineapig_db")
	cursor = cnx.cursor()
	return cnx, cursor


def list_items(item_list):
	long_list = ""
	for row in item_list:
		id = row[0]
		month = row[4].strftime("%B")
		date = f"{month} {row[4].day}, {row[4].year}"
		long_list += f"{list_print.format(id, date, float(row[1]), row[3])}\n"
	# print(long_list)

	subprocess.run(['echo "'+long_list+'" | more'], shell=True)


