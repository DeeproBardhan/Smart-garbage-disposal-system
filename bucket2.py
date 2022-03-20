import http.server
HOST='192.168.0.103'
PORT=8080

class MyHandler(http.server.BaseHTTPRequestHandler):
	id1=0
	points=0
	balance=0
	def do_GET(self):
		print('Connection Established...')
		self.send_responce(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		num=self.rfile.read(10).decode()
		id1,points,balance=Data.database(num)
		print(f'{num}:{id1}\t{points}\t{balance}')
	def do_POST(self):


class Data:
	def database(num):
		con=sqlite3.connect('Dustbin_users.db')
		cursorObj=con.cursor()
		cursorObj.execute('CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY ,phone integer,points integer,balance integer)')
		cursorObj.execute('SELECT phone FROM users where phone=?',(num,))
		data=cursorObj.fetchone()
		if data is None:			
			database_create_user(cursorObj,num,con)

		else:
			cursorObj.execute('SELECT points FROM users where phone=?',(num,))
			data=cursorObj.fetchone()[0]
			if int(data) % 100 == 0:
				database_balance_update(cursorObj,num,con)
			else:
				database_points_update(cursorObj,num,con)
		cursorObj.execute('SELECT id,points,balance FROM users where phone=?',(num,))
		id1=cursorObj.fetchone()[0]
		points=cursorObj.fetchone()[1]
		balance=cursorObj.fetchone()[2]
		con.clear()
		return (id1,points,balance)
			
	def database_points_update(cursorObj,num,con):
		print(f'Updating point of  user {num}')
		cursorObj.execute('UPDATE users SET points=points+10 where phone=?',(num,))
		con.commit()
	def database_balance_update(cursorObj,num,con):
		print(f'Updating balance and point of  user {num}')
		cursorObj.execute('UPDATE users SET points=points+10 ,balance=balance+10 where phone=?',(num,))
		con.commit()
	def database_create_user(cursorObj,num,con):
		print(f'Creating new user {num}')
		cursorObj.execute('INSERT INTO users(phone,points,balance) VALUES(?,?,?)',(num,10,0,))
		con.commit()