# -*- coding: utf-8 -*-
'''
Created on 2017-01-11

@author: zyx
'''

import zmq 
import click

import uuid
import time
import platform
import socket

def sys_version():  
	mac_addr = ':'.join(("%012X" % uuid.getnode())[i:i+2] for i in xrange(0, 12, 2))

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("auto.nie.netease.com",80))
	ip_addr = s.getsockname()[0]
	s.close()

	pc_name = platform.node()
	pc_platform = platform.platform()
	pc_version = platform.version()
	pc_architecture = platform.architecture()[0]

	return mac_addr + '?' + pc_name + '?' + ip_addr + '?' + pc_platform + '?' + pc_version + '?' + pc_architecture

def monitor(sys_info):
	context = zmq.Context()
	monitor_socket = context.socket(zmq.REQ)
	monitor_socket.connect ("tcp://10.246.44.207:10102")
	
	poller = zmq.Poller()
	poller.register(monitor_socket, zmq.POLLIN)

	#print "start monitor"
	click.echo("start monitor")
	message = sys_info
	monitor_socket.send_string(message)
	while True:		
		socks = dict(poller.poll(1000))
		if socks:
			if socks.get(monitor_socket) == zmq.POLLIN:
				#print monitor_socket.recv()
				click.echo(monitor_socket.recv())
				monitor_socket.send_string(message)
		else:
			#print "error: message timeout"
			click.echo("error: message timeout")
		time.sleep(10)

def main(): 
	sys_info = sys_version() 
	click.echo(sys_info)
	monitor(sys_info)

if __name__ == '__main__': 
	main() 