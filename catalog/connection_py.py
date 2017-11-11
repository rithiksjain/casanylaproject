import pymysql

config_local = dict(host='127.0.0.1',user='root',password='root',db='Pieces',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
class connection(object):
	def __init__(self):
		self.config = config_local

	def connect(self):
		try:
			self.conn = pymysql.connect(self.config)
		except Exception as e:
			print (e)
			return dict(status=False,connection="")
		return dict(status=True,connection=self.conn)

	def close_connection(self):
		try:
			self.conn.close()
		except Exception as e:
			print (e)

	def __exit__(self):
		self.close_connection()
