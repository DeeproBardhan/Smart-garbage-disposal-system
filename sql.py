import sqlite3
ID=0
def database(num):
	con=sqlite3.connect('Dustbin_users.db')
	cursorObj=con.cursor()
	cursorObj.execute('CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY ,phone integer,points integer,balance integer)')
	cursorObj.execute('SELECT phone FROM users where phone=?',(num,))
	data=cursorObj.fetchone()
	if data is None:
		print(f'Creating new user {num}')
		database_create_user(cursorObj,num,con)
	else:
		cursorObj.execute('SELECT points FROM users where phone=?',(num,))
		data=cursorObj.fetchone()[0]
		if int(data) % 100 == 0:
			database_balance_update(cursorObj,num,con)
		else:
			database_points_update(cursorObj,num,con)
		
		
def database_points_update(cursorObj,num,con):
		cursorObj.execute('UPDATE users SET points=points+10 where phone=?',(num,))
		con.commit()
def database_balance_update(cursorObj,num,con):
	cursorObj.execute('UPDATE users SET points=points+10 ,balance=balance+10 where phone=?',(num,))
	con.commit()
def database_create_user(cursorObj,num,con):
	cursorObj.execute('INSERT INTO users(phone,points,balance) VALUES(?,?,?)',(num,10,0,))
	con.commit()
def main():
	for i in range(10):
		num=input('Enter number:')
		database(num)
main()