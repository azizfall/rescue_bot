import MySQLdb

def connect():
	conn = MySQLdb.connect(host="localhost",user="rescue_admin",passwd="worldsbestsoccerplayer",db="RescueBot")
	c = conn.cursor()
	return c,conn
