'''
Run:
python client2.py <port_no_of_server_to_connect>


'''


import socket
import sys
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
msg=""
while True:
	received_msg=cs.recv(1024)
	print(received_msg.decode('ascii'),end='\n\n')
	if msg.strip().lower()=='stop':
		break
	msg=input()
	cs.send(msg.encode('ascii'))


cs.close()
