#! /usr/bin/python

import datetime
import os
import sys
import platform
import psutil
import socket
import subprocess

'''af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC',
}'''

DUPLEX_MAP = {
    psutil.NIC_DUPLEX_FULL: "full",
    psutil.NIC_DUPLEX_HALF: "half",
    psutil.NIC_DUPLEX_UNKNOWN: "?",
}

#Display System information
def systemInfo():
		padding = "%-15s %-20s %-20s %-45s %-20s %-20s"
		print(padding % ("OS Name", "Machine Name", "Version#", "Release#", "Hardware name", "Processor name" ))
		print("************************************************************************************************************************************************************")
		#some systems truncate nodename to 8 characters so in that case use socket.gethostname() to get machine name (platform.uname()[1])
		print (padding % ( platform.uname()[0], platform.uname()[1],  platform.uname()[2],  platform.uname()[3], platform.uname()[4], platform.uname()[5]))

#Get Processor information
def cpuInfo():
	cpuinfo = open("/proc/cpuinfo")
	proc = {}
	
	for line in cpuinfo:
		try:
			key,value = line.split(":")
		except:
			break

		key = key.strip()
		value = value.strip()
		if key == "cpu cores":
			proc['cores'] = int(value)
		elif key == "vendor_id":
			proc['id'] = value
		elif key == "model name":
			proc['name'] = value
		elif key == "cpu family":
			proc['family'] = value
		elif key == "model":
			proc['model'] = value
		elif key == "stepping":
			proc['stepping'] = value
		elif key == "cpu MHz":
			proc['mhz'] = value
		elif key == "cache size":
			proc['cache'] = value.split(" ")[0]	
	cpuinfo.close()
	# Get total number of processor. This information is useful if multithreading is enabled or not.
	proc['processors'] = open("/proc/cpuinfo").read().count('processor\t:')
	padding = "%-5s %-5s %-20s %-45s %-15s %-15s %-15s %-15s %-15s"
	print(padding % ("Procs", "Cores", "VendorID", "ModelName", "CpuFamily", "Model",  "Stepping", "CpuSpeed(MHz)", "CacheSize(KB)"))
	print(("************************************************************************************************************************************************************"))
	print(padding % (proc['processors'], proc['cores'], proc['id'], proc['name'], proc['family'],proc['model'],  proc['stepping'], proc['mhz'], proc['cache']))

#Get Memory information
def memoryInfo():
	meminfo = open("/proc/meminfo")
	mem = {}
	for line in meminfo:
		try:
			key,value = line.split(":")
		except:
			break

		value = value.strip()
		if key == "MemTotal":
			mem['total'] = int(value.split(" ")[0])/1024
		elif key == "SwapTotal":
			mem['Swap'] = int(value.split(" ")[0])/1024

	meminfo.close()
	padding = "%-75s %-75s"
	print(padding % ("Total Memory (MB)", "Swap Total (MB)"))
	print(("************************************************************************************************************************************************************"))
	print (padding % (mem['total'], mem['Swap']))

#Get Disk information
def diskInfo():
	df_output_lines = [s.split() for s in os.popen("df -Ph").read().splitlines()]
	length = len(df_output_lines)-1
	padding = "%-30s %-15s %-15s %-15s %-15s %-60s"
	print(padding % ("Filesystem", "Size", "Used", "Available", "Used %", "Mounted on"))
	print(("************************************************************************************************************************************************************"))	
	for i in range(1, length):
		print (padding % (df_output_lines[i][0], df_output_lines[i][1], df_output_lines[i][2], df_output_lines[i][3], df_output_lines[i][4], df_output_lines[i][5]))


#Get Network information	
def networkInfo():
	stats = psutil.net_if_stats()
	padding = "%-5s %-35s %-30s %-45s %-10s %-5s %-10s %-5s"
	print(padding % ("Nic", "Address", "Broadcast","Netmask", "PTP", "Speed", "Duplex", "mtu"))
	print(("************************************************************************************************************************************************************"))
	# Get the Nic and all the addresses associated to it 
	for nic, addrs in psutil.net_if_addrs().items():
		# if NIC exits, return its information regarding ststus, duplex, speed, mtu(bytes)
		if nic in stats: 
			st = stats[nic]
			for addr in addrs:
				print (padding %(nic, addr.address, addr.broadcast, addr.netmask, addr.ptp, stats[nic].speed, DUPLEX_MAP[stats[nic].duplex], stats[nic].mtu))

#Get routing table information
def routingTable():
	route_table = []
	proc = [s.split() for s in os.popen("netstat -r -n").read().splitlines()]
	length = len(proc)
 	#padding = "%-20s %-15s %-15s %-15s %-15s %-15s %-15s"
	#print (padding % ("Network Destination", "Netmask","Gateway", "Flags", "Metric", "Use", "Iface"))
	padding = "%-20s %-15s %-15s %-15s %-15s %-15s %-15s %-15s"
	print (padding % ("Destination", "Gateway", "Getmask", "Flags", "Mss", "Window","irtt", "Iface"))
	print(("************************************************************************************************************************************************************"))
	for i in range(2, length):
		print (padding % (proc[i][0], proc[i][1], proc[i][2], proc[i][3], proc[i][4],proc[i][5], proc[i][6], proc[i][7]))

# Get local user information			
def localUsrs():
	passwd = open("/etc/passwd")
	users = []
	padding = "%-40s %-10s %-70s %-30s"
	print(padding % ("Username", "UserID", "UserIDInfo", "GroupID"))
	print(("************************************************************************************************************************************************************"))
	for i in passwd:
		passwdline = i.strip()
		usr = passwdline.split(":")[0]
		uid = passwdline.split(":")[2]
		grp = passwdline.split(":")[3]
		uinfo = passwdline.split(":")[4]
		print (padding %(usr, uid, uinfo, grp))
					
# Get local group information
def localGroup():
	grp = open("/etc/group")
	padding = "%-30s %-30s %-100s"
	print(padding % ("GroupName", "GroupID", "GroupList"))
	print(("************************************************************************************************************************************************************"))
	for i in grp:
		localgroup = i.strip()
		grpName = localgroup.split(":")[0]
		grp = localgroup.split(":")[2]
		grpList = localgroup.split(":")[3]
		print (padding %(grpName, grp, grpList))


#Print out all the information
def main():
	#today = datetime.datetime.today()
	#print "Encoding is", sys.stdin.encoding
	print ("************************************************************************************************************************************************************")
	print ("                                                                 "+datetime.datetime.today().strftime('Date %d/%m/%Y %H:%M:%S'))
	print ("************************************************************************************************************************************************************")
	print ("                                                                      System Information")
	print ("************************************************************************************************************************************************************")
	systemInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                       CPU Information")
	print ("************************************************************************************************************************************************************")
	cpuInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                      Memory Information")
	print ("************************************************************************************************************************************************************")
	memoryInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                       Disk Information")
	print ("************************************************************************************************************************************************************")
	diskInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                     Network Information")
	print ("************************************************************************************************************************************************************")
	networkInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                     Routing table Information")
	print ("************************************************************************************************************************************************************")
	routingTable()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                     Local User Information")
	print ("************************************************************************************************************************************************************")
	localUsrs()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                     Local Group Information")
	print ("************************************************************************************************************************************************************")
	localGroup()
	print ("")
	
if __name__ == '__main__':
	main()