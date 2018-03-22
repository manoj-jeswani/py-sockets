'''
Server to host a chat room

Run: python3 <script_name>.py port_no

to test it open up multiple terminals and: 
telnet host_ip port
every individual's msg would be broadcasted.

'''

import socket
import datetime
import threading
import sys

def handle_client(cs,addr,host_ip,cs_list):
	msg="Hello client {0}.You have entered into chat room.Start texting..\nHit 'Exit' to leave chat room.\n".format(addr)
	cs.send(msg.encode('ascii'))

	while True:
		cmsg=cs.recv(4096).decode('ascii')
		if cmsg.strip().lower()=='exit':
			break
		
		to_send_all="({}) [{}:{}] : {}\n".format(str(datetime.datetime.now()),addr[0],addr[1],cmsg)

		list(map(lambda x:x.send(to_send_all.encode('ascii')),filter(lambda x:x!=cs,cs_list))) #sending msg to all the clients except the current client
		

	msg="Closing Connection.Exiting from chat room.\n" 
	cs.send(msg.encode('ascii'))	
	cs.close()
	print('Connection closed with client ',addr)
	if cs in cs_list:
		cs_list.remove(cs)



def main():

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
	print('Server started listening on port ',port)
	#cs-> client-socket
	#add[0]--> ip add. of host ,addr[1] --> port number
	thread_list=[]
	cs_list=[]
	while True:
		cs,addr=ss.accept()
		print('Connection established with client ',addr)
		cs_list.append(cs)
		t=threading.Thread(target=handle_client,args=(cs,addr,host_ip,cs_list),name='client-{}-thread'.format(addr))
		t.start()
		thread_list.append(t)

	list(map(lambda x:x.join(),thread_list))
	ss.close()

if __name__=="__main__":
	main()
