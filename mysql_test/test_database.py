import sqlite3

conn = sqlite3.connect('money.db')
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS results(id INTEGER AUTO_INCREMENT,class_name INTEGER, PRIMARY KEY (id))')

def data_entry():
	c.execute('INSERT INTO results (class_name) VALUES(2)')
	conn.commit()
	c.close()
	conn.close()

create_table()
data_entry()