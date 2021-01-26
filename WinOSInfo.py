# -*- coding: utf-8 -*-

#*****************************************************************************************************************
# If this script fails to run fully, you will need to set Pythonencoding to utf-8 via command prompt. Following are the commands
# > chcp 65001
# > set PYTHONIOENCODING=utf-8
#*****************************************************************************************************************
import datetime
import os
import sys
import platform
import wmi  #You will need to download wmi package to use it. This can be downloaded from https://pypi.python.org/pypi/WMI/#downloads
import win32com.client
import psutil

strComputer = "."

#Display System information
def systemInfo():
		padding = "%-20s %-15s %-15s %-15s %-20s %-45s"
		print(padding % ("OS Name", "Machine Name", "Version#", "Release#", "Hardware name", "Processor name" ))
		print("************************************************************************************************************************************************************")
		#some systems truncate nodename to 8 characters so in that case use socket.gethostname() to get machine name (platform.uname()[1])
		print (padding % ( platform.uname()[0], platform.uname()[1],  platform.uname()[2],  platform.uname()[3], platform.uname()[4], platform.uname()[5]))

#Get Processor information
def cpuInfo():
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_Processor")
	padding = "%-42s %-38s %-10s %-10s %-10s %-10s %-10s %-15s"
	print(padding % ("Name", "Description", "ExtClock", "L2CacheSize","MaxFreq",  "#OfPCores", "#OfLCores", "SocketDesignation"))
	print("************************************************************************************************************************************************************")
	for objItem in colItems:
		print (padding % (objItem.Name, objItem.Description, objItem.ExtClock, objItem.L2CacheSize, objItem.MaxClockSpeed,   objItem.NumberOfCores, objItem.NumberOfLogicalProcessors, objItem.SocketDesignation))

#Get Memory information
def memoryInfo():
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_PhysicalMemory")
	padding = "%-30s %-25s %-25s %-25s %-25s %-25s"
	print(padding % ("Name", "BankLabel", "Capacity(MB)", "FormFactor", "MemoryType", "Speed"))
	print("************************************************************************************************************************************************************")
	for objItem in colItems:
		print (padding % (objItem.Name, objItem.BankLabel, int(objItem.Capacity)/(1024 * 1024), objItem.FormFactor, objItem.MemoryType, objItem.Speed))
	
	print ("")
	print ("Total Memory in MB: ", psutil.virtual_memory()[0]/(1024 * 1024)) #returns Total memory in MB
	print ("Current Available Memory in MB: ", psutil.virtual_memory()[1]/(1024 * 1024)) #returns available memory in MB
	
#Get Disk information
def diskInfo():
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
    colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_LogicalDisk")
    padding = "%-40s %-45s %-45s %-20s"
    print(padding % ("Drive Name", "Size (GB)", "Free Space (GB)", "File System"))
    print("************************************************************************************************************************************************************")
    for objItem in colItems:
        if objItem.Size == None:
            print (padding % ( objItem.Name, "None", "None",  objItem.FileSystem))
        else:
            Size = int(objItem.Size)/(1024 * 1024 * 1024)
            FreeSpace = int(objItem.FreeSpace)/(1024 * 1024 * 1024)
            print (padding % ( objItem.Name, Size, FreeSpace,  objItem.FileSystem))

#Get Network information	
def networkInfo():
		objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
		objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
		colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_NetworkAdapterConfiguration")
		padding = "%-45s %-15s %-15s %-15s %-20s %-17s %-17s"
		print(padding % ("Description", "DHCPServer", "DHCPDomain","DNSHostName", "MACAddress", "WINSPrimaryServer", "WINSSecondaryServer"))
		print("************************************************************************************************************************************************************")
		for objItem in colItems:
			print (padding % ( objItem.Description, objItem.DHCPServer, objItem.DNSDomain, objItem.DNSHostName, objItem.MACAddress, objItem.WINSPrimaryServer, objItem.WINSSecondaryServer))

#Get Window services information
def windowServicesInfo():
	padding = "%-40s %-70s %-20s %-20s"
	print(padding % ("SERVICE NAME", "DISPLAY NAME", "START TYPE", "STATUS"))
	print("************************************************************************************************************************************************************")
	result = list(psutil.win_service_iter())
	print ("Total Services installed: ", len(result))
	for item in result:
		print (padding % (item.name(),item.display_name(), item.start_type(), item.status()))
	print ("")
	
#Display list of all the installed program	
def installedPrgInfo():
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
	colItems = objSWbemServices.ExecQuery("Select Name, Vendor, Version, InstallDate from Win32_Product WHERE Name <> Null")
	padding = "%-80s %-40s %-20s %-10s"
	print(padding % ("NAME", "VENDOR", "VERSION", "INSTALL DATE"))
	print("************************************************************************************************************************************************************")
	print ("Total # of programs installed: ", len(colItems))
	for objItem in colItems:
		print (padding % (objItem.Name,objItem.Vendor,objItem.Version, objItem.InstallDate))
		
#Display list of all the hot fixes	
def hotFixInfo():
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
	colItems = objSWbemServices.ExecQuery("Select Caption, Description, HotFixID, InstalledOn, InstalledBy from Win32_QuickFixEngineering")
	padding = "%-70s %-20s %-20s %-20s %-20s"
	print(padding % ("CAPTION", "DESC", "HOTFIX_ID", "INSTALL DATE", "INSTALLED BY"))
	print("************************************************************************************************************************************************************")
	print ("Total # of hotfixes: ",len(colItems))
	for objItem in colItems:
		print (padding % (objItem.Caption, objItem.Description,objItem.HotFixID, objItem.InstalledOn, objItem.InstalledBy))
		
#Display list of all the startup commands	
def startupCommandInfo():
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator") 
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2") 
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_StartupCommand")
	padding = "%-50s %-100s"
	print(padding % ("NAME", "COMMAND"))
	print("************************************************************************************************************************************************************")
	for objItem in colItems:
		print (padding % (objItem.Name,objItem.command))
		
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
	print ("                                                                    Memory Information")
	print ("************************************************************************************************************************************************************")
	memoryInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                    Disk Information")
	print ("************************************************************************************************************************************************************")
	diskInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                   Network Information")
	print ("************************************************************************************************************************************************************")
	networkInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                Window Services Installed")
	print ("************************************************************************************************************************************************************")
	windowServicesInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                Window Programs Installed")
	print ("************************************************************************************************************************************************************")
	installedPrgInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                    Hot fix Installed")
	print ("************************************************************************************************************************************************************")
	hotFixInfo()
	print ("")
	print ("************************************************************************************************************************************************************")
	print ("                                                                      Startup Commands")
	print ("************************************************************************************************************************************************************")
	startupCommandInfo()
	print ("")

	
if __name__ == '__main__':
	main()
	