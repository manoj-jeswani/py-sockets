'''
scans for open ports (in range [1,10000]) 
for a given server in a multithreaded fashion 

'''
import socket
import threading

def pscan(s,host_ip,port):
	try:
		s.connect((host_ip,port))
		return True
	except:
		return False


def range_scanner(s,begin,end,host_ip,l):
	global open_port_list
	for i in range(begin,end+1):
		if pscan(s,host_ip,i):
			l.acquire()
			open_port_list.append(i)
			l.release()




open_port_list=[]

def main():
	global open_port_list
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host='www.hackthissite.org'
	host_ip=socket.gethostbyname(host)
	l=threading.Lock()
	thread_list=[]
	for i in range(100): #each thread scans 100 ports
		t=threading.Thread(target=range_scanner,args=(s,i*100+1,(i+1)*100,host_ip,l),name="t-{}".format(i))
		t.start()
		thread_list.append(t)

	list(map(lambda x:x.join(),thread_list))
	print(open_port_list)






if __name__=="__main__":
	main()