#!/usr/bin/python

import paramiko
import time
import re
import argparse

RCV_BUFFER = 65535
TIME_DELAY = 1
#eceive Switch Attributes: IPAddress, Username and Password

AttributeParser = argparse.ArgumentParser()
AttributeParser.add_argument("VDXIP",help='VDX management IP')
AttributeParser.add_argument("--Username",'-u',help='VDX Login Username')
AttributeParser.add_argument("--Password",'-p',help='VDX Login Password')

SwitchAttributes = AttributeParser.parse_args()

#Use VDX default Username and Password if none specified as inputs

if SwitchAttributes.Username:
	username = SwitchAttributes.Username
else:
	username = 'admin'

if SwitchAttributes.Password:
	password = SwitchAttributes.Password
else:
	password = 'password'


def SSHConnect_to_VDX(ip,username,password):

	'''
	Using the login attributes connect to remote VDX switch over SSH using Paramiko Library. The function will also set the paging length of the NOS CLI shell to 0.
	'''

#Paramiko SSH Client Object

	VdxConnectionObj = paramiko.SSHClient()

#Ignore SSH Host key 

	VdxConnectionObj.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Initiate SSH Connection to remote VDX device

	try:
		VdxConnectionObj.connect(ip,username=username,password=password)

	except Exception as Err:
		print "SSH Connection to switch failed:", type(Err), Err


#Invoke NOS CLI shell with remote VDX

	try:	
		NOSConnectionObj = VdxConnectionObj.invoke_shell()
		print "Connection to NOS CLI Successful\n"
	
	except Exception as Err:
		print "CLI Connection to NOS Shell Failed:",type(Err),Err


#Read Initial Screen Output buffer and Discard

	NOSConnectionObj.recv(RCV_BUFFER)

	Disable_Paging(NOSConnectionObj)

	LargeFileNames = Find_Large_Files(NOSConnectionObj)	
	print LargeFileNames

#Close SSH Connection Object
	try:
		VdxConnectionObj.close()
		print "SSH Connection to VDX Closed Successfully\n"
	except SSHConnectionCloseError as Err:
		print "Error Closing SSH Connection:",type(Err),Err

def Disable_Paging(NOSConnectionObj):
	'''
	Set the CLI Page length to 0 to disable Paging
	'''

	command = 'terminal length 0'

	NOSConnectionObj.send("\n")
	time.sleep(TIME_DELAY)
	NOSConnectionObj.recv(RCV_BUFFER)
	
	try:
		NOSConnectionObj.send(command)
		time.sleep(TIME_DELAY)

	except Exception as Err:
		print "Could not set Terminal Length to 0:",type(Err), Err
	
	output = NOSConnectionObj.recv(RCV_BUFFER)
	print output,'\n\n'

	return


def Find_Large_Files(NOSConnectionObj):

	'''
		Identify Space consuming files on VDX Compact Flash
	'''
#Unhide the FOS Command shell to execute root level commands

	FOS_Command = 'unhide foscmd\n'
	FOS_Password = 'fibranne\n'
	
	NOSConnectionObj.send('\n')
	time.sleep(TIME_DELAY)

	NOSConnectionObj.send(FOS_Command)
	time.sleep(TIME_DELAY)

	NOSConnectionObj.send(FOS_Password)
	time.sleep(TIME_DELAY)

	NOSConnectionObj.send('foscmd "find / -path /mnt -prune -o -printf \'%s%p\\n\' | sort -nr | head"\n')
	print "Finding Files consuming disk space...\n"
	time.sleep(TIME_DELAY+5)
	
	output = NOSConnectionObj.recv(RCV_BUFFER)
	
	type(output)

	return output

SSHConnect_to_VDX(SwitchAttributes.VDXIP,username,password)






