import socket
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

port=8080
ss.bind((host_ip,port))
print("Server socket binded to %s:%d"%(host_ip,port))
ss.listen(10)
print('Server started lsitening on port ',port)
#cs-> client-socket
#add[0]--> ip add. of host ,addr[1] --> port number
cs,addr=ss.accept()
print('Connection established with client ',addr)
msg="Hello client {0} from server {1}".format(addr,host_ip)
cs.send(msg.encode('ascii'))
cs.close()
ss.close()