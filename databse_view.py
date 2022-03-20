import sqlite3 as lite

conn = lite.connect('Dustbin_users.db')
cur = conn.cursor()

def get_posts():
    with conn:
        cur.execute("SELECT * FROM users")
        num=1
        while(cur.fetchall()[num]!=0):
        	print(cur.fetchall()[num])
        	#print()
        	num=num+1

get_posts()