import MySQLdb

try:
	conn = MySQLdb.connect(host='192.168.42.1',user='root',passwd='heng130509',db='mysql',port=3306)
	cor = conn.cursor()
	cor.execute('select * from user')
	cor.close()
	conn.close()
except MySQLdb.Error, e:
	print "MySQLdb Error %d:%s" %(e.args[0],e.args[1])
