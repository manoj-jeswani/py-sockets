'''
Run:
python server2.py <port_no_to_bind>


To verify that this server is entertaining only one client at a time:
open another terminal and do telnet on the server , it will not reply bcoz 
currently its busy in connection with 1st client when that client will stop server will come out of loop
and will accept 2nd client's conection then as connection to 1st client would have been closed.

here main server after accepting connection gets busy with that and no one os there to accept new one.....
'''


import socket
import datetime
import os
import sys
#ss-> server socket
try:
	ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print('server socket created')
except socket.error as e:
	print(e)


host=socket.gethostname()

try:
	host_ip=socket.gethostbyname(host)
except socket.gaierror as e:
	print('Unable to resolve hostname and get IP...Using hostname for Connection')
	host_ip=host

try:
	port=int(sys.argv[1])
except:
	print('Invalid port number')
	sys.exit()

ss.bind((host_ip,port))
print("Server socket binded to %s:%d"%(host_ip,port))
ss.listen(10)
print('Server started lsitening on port ',port)
#cs-> client-socket
#add[0]--> ip add. of host ,addr[1] --> port number
fname=None

while True:
	cs,addr=ss.accept()
	print('Connection established with client ',addr)
	msg="Hello client {0}.You are connected to server {1}\nNow you may send messages,that gonna be stored on server\n with timestamp.To terminate send 'Stop'.\n".format(addr,host_ip)
	cs.send(msg.encode('ascii'))
	fname='client-{}:{}.txt'.format(addr[0],addr[1])
	with open(fname,'a+') as f:
		while True:
			cmsg=cs.recv(4096).decode('ascii')
			if cmsg.strip().lower()=='stop':
				msg="Closing Connection\n" 
				cs.send(msg.encode('ascii'))	
				cs.close()
				print('Connection closed with client ',addr)
				break
			to_write=str(datetime.datetime.now())+" => "+cmsg+"\n"
			f.write(to_write)
			msg=str('Saved.... "'+to_write.strip()+'"\n').encode('ascii')
			cs.send(msg)


cs.close()
ss.close()