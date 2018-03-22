'''
Run:
python client5.py <port_no_of_server_to_connect>
in multiple terminals and interact with server from each terminal.

2 threads ar made to concurrently read and write to terminal
'''

import socket
import sys
import threading

flag=1

def receive_write(cs):
	while flag:
		received_msg=cs.recv(1024)

		sys.stdout.write('\n'+received_msg.decode('ascii')+"\n")



def read_send(cs):
	global flag
	while True:
		msg=sys.stdin.readline()
		cs.send(msg.encode('ascii'))
		if msg.strip().lower()=='stop':
			flag=0
			break



def main():

	cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_to_connect=socket.gethostname()

	try:
		port=int(sys.argv[1])
	except:
		print('Invalid port number')
		sys.exit()

	try:
		cs.connect((server_to_connect,port))
	except ConnectionRefusedError as e:
		print('Server {} denied to connect at port {}'.format(server_to_connect,port))
		sys.exit()

	print('connection esatblished with server {}'.format(server_to_connect))
	rwt=threading.Thread(target=receive_write,args=(cs,))
	rst=threading.Thread(target=read_send,args=(cs,))
	rwt.start()
	rst.start()
	rwt.join()
	rst.join()
	cs.close()


if __name__=="__main__":
	main()