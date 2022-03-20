import socket,os,time,sqlite3
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='192.168.43.31'
ID=0

def connection():
	PORT=int(input('Enter PORT:'))
	try:
		s.bind((HOST,PORT))
		print(f"Server started at {HOST},{PORT}")
		s.listen(1)
		clientsocket,address =s.accept()
		print(f"Connection from {address} has been estabilished[].....")
		print('Now users can throw garbage.Woohohoh!')
		bucket(clientsocket)
	except Exception as e:
		print(f'Exception occured:{e}\n Trying Again...')
		time.sleep(1)
		connection()


def bucket(clientsocket):

	USER_NO=1
	while True:		
		print(f"User{USER_NO}:")
		number=clientsocket.recv(10).decode()
		print(number)
		if(len(number)==10):
			points=database(number)
			#print(f'{num}:{id1}\t{points}\t{balance}')
			
			# pts=str(points)
			print(points)
			points=str(points)
			points=";"+points+";\n"
			time.sleep(2)
			print(f'Points:{points}')
			clientsocket.send((points).encode())
			USER_NO+=1
		else:
			continue
	

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
	cursorObj.execute('SELECT points FROM users where phone=?',(num,))
	points=cursorObj.fetchone()[0]
	return (points)
		
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

connection()