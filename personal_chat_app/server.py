'''
Personal chat system

'''
import pymysql
import socket
import datetime
import threading
import sys
import re

def signup(cs,cu,mapper,db):
	msg='Enter name, username and password separated by a space\n'
	cs.send(msg.encode('ascii'))

	while 1:
		try:
			name,uname,password=cs.recv(4096).decode('ascii').strip().split()
		except:
			msg='Enter name,username and password again\n'
			cs.send(msg.encode('ascii'))
			continue
		
		if (not uname.isalnum()) or (not password.isalnum()) or (not name.isalnum()):
			msg='Enter name,username and password again\n'
			cs.send(msg.encode('ascii'))
			continue


		query="select * from users where uname='%s'"%(uname)
		cu.execute(query)
		res=cu.fetchall()
		if not res:
			query='insert into users values("%s","%s","%s")'%(name,uname,password)
			try:
				cu.execute(query)
				db.commit()
			except:
				db.rollback()

			msg='User with username %s registered successfully..\n'%(uname)
			cs.send(msg.encode('ascii'))
			mapper[uname]=cs
			break
		else:
			msg='User already exists...Enter name,username and password again\n'
			cs.send(msg.encode('ascii'))
	return uname



def login(cs,cu,mapper):
	msg='Enter username and password separated by a space\n'
	cs.send(msg.encode('ascii'))

	while 1:
		try:
			uname,password=cs.recv(4096).decode('ascii').strip().split()
		except:
			msg='Enter username and password again\n'
			cs.send(msg.encode('ascii'))
			continue
		
		if not uname.isalnum():
			msg='Enter username and password again\n'
			cs.send(msg.encode('ascii'))
			continue


		query="select * from users where uname='%s' and pass='%s'"%(uname,password)
		cu.execute(query)
		res=cu.fetchall()
		print(res)
		if res:
			msg='User with username %s logged in successfully..\n'%(uname)
			cs.send(msg.encode('ascii'))
			mapper[uname]=cs
			break
		else:
			msg='Wrong username or password...Enter username and password again\n'
			cs.send(msg.encode('ascii'))
	return uname		


def getTargetUserAndMsg(cmsg):
	tobj=re.search(r'^<(.*)>(.*)$',cmsg,re.M|re.I)
	return tobj.groups()


def handle_client(cs,addr,cu,mapper,db):
	msg="Hello client {0}.\nHit 1 for signup , 2 for login\n".format(addr)
	cs.send(msg.encode('ascii'))
	uname=""
	while True:
		try:
			cmsg=int(cs.recv(1024).decode('ascii').strip())
		except:
			msg="Invalid input.."
			cs.send(msg.encode('ascii'))

			sys.exit()

		if cmsg==1:
			uname=signup(cs,cu,mapper,db)
			break
		elif cmsg==2:
			uname=login(cs,cu,mapper)
			break
		else:
			msg="Wrong choice.. enter again\n"
			cs.send(msg.encode('ascii'))

	msg="You can begin texting..\n each of your message should begin with username of target user enclosed between <>\ni.e. Format is: <username> your message...\nHit 'Stop' to exit\n "
	cs.send(msg.encode('ascii'))
	while True:
		cmsg=cs.recv(4096).decode('ascii').strip()
		if cmsg.lower()=='stop':
			break
		
		try:

			tup=getTargetUserAndMsg(cmsg)
		except:
			msg="Invalid input...Send again"
			cs.send(msg.encode('ascii'))
			continue


		to_send_target="({}) [{}] : {}\n".format(str(datetime.datetime.now()),uname,tup[1])
		
		if tup[0] in mapper:

			tcs=mapper[tup[0]]
			tcs.send(to_send_target.encode('ascii'))
		else:
			msg="User with username %s offline..Unable to send message..\n"%(tup[0])
			cs.send(msg.encode('ascii'))

	msg="Closing Connection.Exiting....\n" 
	cs.send(msg.encode('ascii'))	
	cs.close()
	del mapper[uname]
	print('Connection closed with client ',addr)
	



def main(cu,db):

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
	mapper={}
	while True:
		cs,addr=ss.accept()
		print('Connection established with client ',addr)
		t=threading.Thread(target=handle_client,args=(cs,addr,cu,mapper,db),name='client-{}-thread'.format(addr))
		t.start()
		thread_list.append(t)

	list(map(lambda x:x.join(),thread_list))
	ss.close()

if __name__=="__main__":
	db=pymysql.connect("127.0.0.1","root","rope","pchat")
	cu=db.cursor()
	main(cu,db)
	db.close()
	
