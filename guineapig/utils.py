import mysql.connector


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