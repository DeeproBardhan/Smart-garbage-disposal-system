import socket,os,time,sqlite3
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='192.168.0.104'
PORT=44457
ID=0
#USER_NO=1
def bind():
	try:
		s.bind((HOST,PORT))
		print(f'Server starteed at {HOST}:{PORT}')
		listen()
	except:
		print(f'Exception occured in bind()={Exception}')
		print('Trying again...')
		time.sleep(1)
		bind()

def listen():
	try:
		s.listen(1)
		clientsocket,address=s.accept()
		print(f'New Connection from {address}')
		print('Now users can throw garbage.Woohohoh!')
		bucket(clientsocket)
	except:
		print(f'Exception occured in listen()={Exception}')
		print('Trying again...')
		listen()


def bucket(clientsocket):
	# while True:		
	#print(f"User{USER_NO}:")
	number=clientsocket.recv(10).decode()
	print(number)
	id1,points,balance=database(number)
	print(f'{num}:{id1}\t{points}\t{balance}')
	clientsocket.send(points)
	#USER_NO+=1
	#clientsocket.send(balance)
	

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

bind()