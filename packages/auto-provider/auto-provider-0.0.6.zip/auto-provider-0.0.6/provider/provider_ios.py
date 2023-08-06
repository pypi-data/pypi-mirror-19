import zmq 
import click

import socket
import time
import platform
import subprocess

import config

def getIpAddress():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("auto.nie.netease.com",80))
	ip_addr = s.getsockname()[0]
	s.close()
	return ip_addr

def trace():
	proc = subprocess.Popen(["system_profiler", "SPUSBDataType"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	out = proc.communicate()[0].strip()
        results = out.split("\n")
	udids = []
	for result in results:
		if (result.find('Serial Number') != -1):
			udids.append(result.split(": ")[1]) 
	return udids 


def getInfo(udid, ipAddress):
	proc = subprocess.Popen(['ideviceinfo', '-u', udid], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	out = proc.communicate()[0].strip()
	results = out.split("\n")

	model = 'unkown'
	version = 'unkown'
	sdk = 'unkown'
        for result in results:
		if (result.startswith('ProductType')):
			model = config.iOS_map[result[13:]]
			version = result[13:]
		if (result.startswith('ProductVersion')):
			sdk = result[16:]
	return udid + '?' + model + '?' + version + '?' + sdk + '?' + ipAddress 
	

def main():
	click.echo(platform.system())
	ipAddress = getIpAddress()
	cache_udids = []

	context = zmq.Context()
	monitor_socket = context.socket(zmq.REQ)
	monitor_socket.connect ("tcp://10.246.44.207:10103")

	poller = zmq.Poller()
	poller.register(monitor_socket, zmq.POLLIN)
	
	click.echo("start monitor")
	while (True):
		udids = trace()
		for udid in udids:
			deviceInfo = getInfo(udid, ipAddress)
			#click.echo(deviceInfo)
			monitor_socket.send(deviceInfo)	
			socks = dict(poller.poll(1000))
			if socks:
				if socks.get(monitor_socket) == zmq.POLLIN:
					click.echo(monitor_socket.recv())
			else:
				click.echo("error: message timeout")	
		#for udid in udids:
		#	if (udid in cache_udids):
		#		click.echo('heartbeat----' + udid)
		#		monitor_socket.send('2?' + udid)
		#		socks = dict(poller.poll(1000))
		#		if socks:
		#			if socks.get(monitor_socket) == zmq.POLLIN:
		#				click.echo(monitor_socket.recv())
		#		else:
		#			click.echo("error: message timeout")	
		#	else:
		#		click.echo('introduction----' + udid)
		#		deviceInfo = getInfo(udid, ipAddress)
		#		click.echo(deviceInfo)
		#		monitor_socket.send('1?' + deviceInfo)	
		#		socks = dict(poller.poll(1000))
		#		if socks:
		#			if socks.get(monitor_socket) == zmq.POLLIN:
		#				click.echo(monitor_socket.recv())
		#		else:
		#			click.echo("error: message timeout")	
		#for udid in cache_udids:
		#	if (udid not in udids):
		#		click.echo('absent----' + udid)
		#		monitor_socket.send('3?' + udid)	
		#		socks = dict(poller.poll(1000))
		#		if socks:
		#			if socks.get(monitor_socket) == zmq.POLLIN:
		#				click.echo(monitor_socket.recv())
		#		else:
		#			click.echo("error: message timeout")	
		#cache_udids = udids
		time.sleep(10)	


if __name__ == '__main__': 
	main() 
