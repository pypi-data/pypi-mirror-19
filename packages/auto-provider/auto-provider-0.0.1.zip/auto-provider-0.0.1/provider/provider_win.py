# -*- coding: utf-8 -*-
'''
Created on 2017-01-11

@author: zyx
'''

import wmi 
import netifaces
import zmq 
import time
import platform
import socket

def sys_version():  
	c = wmi.WMI()
	eth = netifaces.interfaces()[0]
	mac_addr = netifaces.ifaddresses(eth)[netifaces.AF_LINK]
	result =mac_addr[0]['addr']
	result = result	+ "?"+ platform.node()

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("auto.nie.netease.com",80))
	myaddr = s.getsockname()[0]
	result = result	+ "?"+ myaddr
	s.close()

	for sys in c.Win32_OperatingSystem(): 
		result = result + "?" + sys.Caption 
		result = result + "?" + sys.BuildNumber 
		result = result + "?" + sys.OSArchitecture 
	return result 

def monitor(sys_info):
	context = zmq.Context()
	monitor_socket = context.socket(zmq.REQ)
	monitor_socket.connect ("tcp://10.246.44.207:10102")
	
	poller = zmq.Poller()
	poller.register(monitor_socket, zmq.POLLIN)

	print "start monitor"
	message = sys_info
	monitor_socket.send_string(message)
	while True:		
		socks = dict(poller.poll(1000))
		if socks:
			if socks.get(monitor_socket) == zmq.POLLIN:
				print monitor_socket.recv()
				monitor_socket.send_string(message)
		else:
			print "error: message timeout"
		time.sleep(10)

def main(): 
	sys_info = sys_version() 
	monitor(sys_info)

if __name__ == '__main__': 
	main() 