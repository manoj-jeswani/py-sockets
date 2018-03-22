import socket
import sys
cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_to_connect=socket.gethostname()
port=8080

try:
	cs.connect((server_to_connect,port))
except ConnectionRefusedError as e:
	print('Server {} denied to connect at port {}'.format(server_to_connect,port))
	sys.exit()

print('connection esatblished with server {}'.format(server_to_connect))
received_msg=cs.recv(1024)
print("message received is : ",received_msg.decode('ascii'))
cs.close()