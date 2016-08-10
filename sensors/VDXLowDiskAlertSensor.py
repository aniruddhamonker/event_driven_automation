#!/usr/bin/python

import socket
import time
import re
import pprint
from st2reactor.sensor.base import Sensor

if __name__ == '__main__':

	class SyslogSensor(Sensor):

	    def __init__(self):
	        super(SyslogSensor, self).__init__(sensor_service=sensor_service)
		self._trigger_ref = 'NOS.LowDiskAlert'

	    def setup(self):	
	        self.ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		try:
		    self.ServerSocket.bind(('0.0.0.0',514))
	            print("Server binding Successful \n")
		except Exception as e:
                    print "Error Binding the server:",type(e),e
			
	    def run(self):
	    	while True:
		    data,self.ClientAddress = self.ServerSocket.recvfrom(65535)
		    FilterData = re.search('<\d+>(?P<DATE>\w+\s+\d{1,2} [\d\+:]+).*(?P<MSG_ID>\[msgid@.*?\]).*(?P<DEVICE>\[attr@.*?\]).*(?P<SEVERITY>\[severity@.*?\]).*\[swname@.*value=(?P<HOSTNAME>\".+?\")\].*BOM\s?(?P<SYSLOG>.*)',str(data))	
			
	            try:
		        if 'FW-1402' in FilterData.group('MSG_ID'):
        	            print ("Low Disk Space reported on Switch with IP address %s\n")%(self.ClientAddress)
                	    TriggerLowDiskAlert()
		    except Exception as e:
                        pass

 		    time.sleep(0.5)

			
	    def TriggerLowDiskAlert(self):
	        trigger = self._trigger_ref
		payload = {
		 	      'ClientAddress' : self.ClientAddress
			  } 

		try:
		    self.sensor_service.dispatch(trigger=trigger,payload=payload)
		except Exception as e:
		    print "Failed to dispatch Trigger:",type(e),e

            def cleanup(self):
	        self.ServerSocket.close()

	    def add_trigger(self, trigger):
	        pass

            def update_trigger(self, trigger):
	        # This method is called when trigger is updated
		pass

	    def remove_trigger(self, trigger):
	        # This method is called when trigger is deleted
		pass


