#!/usr/bin/python

import paramiko
import time
from st2actions.runners.pythonrunner import Action

RCV_BUFFER = 65535
TIME_DELAY = 1

class SSHConnectToVDX(Action):
    def __init__(self,VDX_IpAddr,username='admin',password='password',config=None,action_service=None):
        super(SSHConnectToVDX,self).__init__(config=config,action_service=action_service)

        self.username = username
	self.password = password
	self.ip_addr = VDX_IpAddr

    def run(self):
#Paramiko SSH Client Object
        VdxConnectionObj = paramiko.SSHClient()
#Ignore SSH Host key
        VdxConnectionObj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#Initiate SSH Connection to remote VDX device
        try:
            VdxConnectionObj.connect(self.ip_addr,username=self.username,password=self.password)
        except Exception as Err:
            print "SSH Connection to switch failed:", type(Err), Err
#Invoke NOS CLI shell with remote VDX
	try:
            CLIConnectionObj = VdxConnectionObj.invoke_shell()
            print "Connection to NOS CLI Successful\n"
        except Exception as Err:
            print "CLI Connection to NOS Shell Failed:",type(Err),Err
#Read Initial Screen Output buffer and Discard
	CLIConnectionObj.recv(RCV_BUFFER)
#Disable cli output paging on the VDX
        _disable_Paging(CLIConnectionObj)
#Get names of the top 5 disk space consuming files from VDX
        LargeFileNames = _find_large_files(CLIConnectionObj)
        print LargeFileNames
#Close SSH Connection Object
        try:
            VdxConnectionObj.close()
            print "SSH Connection to VDX Closed Successfully\n"
        except SSHConnectionCloseError as Err:
            print "Error Closing SSH Connection:",type(Err),Err

    def _disable_Paging(self,CLIConnectionObj):
        '''
        Set the CLI Page length to 0 to disable Paging
        '''
        command = 'terminal length 0'
        CLIConnectionObj.send("\n")
        time.sleep(TIME_DELAY)
        CLIConnectionObj.recv(RCV_BUFFER)
	try:
            CLIConnectionObj.send(command)
            time.sleep(TIME_DELAY)
        except Exception as Err:
            print "Could not set Terminal Length to 0:",type(Err), Err
	output = CLIConnectionObj.recv(RCV_BUFFER)
        print output,'\n\n'

    def _find_large_files(self,CLIConnectionObj):
        '''
                Identify Space consuming files on VDX Compact Flash
        '''
#Unhide the FOS Command shell to execute root level commands
        FOS_Command = 'unhide foscmd\n'
        FOS_Password = 'fibranne\n'

        CLIConnectionObj.send('\n')
        time.sleep(TIME_DELAY)
        CLIConnectionObj.send(FOS_Command)
        time.sleep(TIME_DELAY)
        CLIConnectionObj.send(FOS_Password)
        time.sleep(TIME_DELAY)

        CLIConnectionObj.send('foscmd "find / -path /mnt -prune -o -printf \'%s%p\\n\' | sort -nr | head"\n')
        print "Finding Files consuming disk space...\n"
        time.sleep(TIME_DELAY+5)
        output = CLIConnectionObj.recv(RCV_BUFFER)
        return output


        
