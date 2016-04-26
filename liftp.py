#!/usr/bin/python

import os
import sys
import ftplib
import socket

class Myftp:
    def __init__(self,user,Pass,localpath,host,port=21):
        self.host = host
	self.port = port 
	self.user = user
	self.Pass = Pass
	self.localpath = localpath

    def Connect(self):
        ftp = ftplib.FTP()
	ftp.set_pasv(True) //是否开启被动模式
	try:
	    ftp.connect(self.host,self.port)
	except socket.error,e:
	    print e
	else:
	    try:
                ftp.login(self.user,self.Pass)
	    except:
	        print 'username or password error..'
            return ftp

    def loadfile(self):
        ftps = self.Connect()
	bufsize = 1024
	remotepath = ftps.pwd()
	for localdir in os.walk(self.localpath):
	    if not ''.join(localdir[0].split(os.sep)[2:]).startswith('.'):
	        for subdirs in os.listdir(localdir[0]):
		    if os.path.isdir(os.path.join(localdir[0],subdirs)):
		        try:
		            ftps.mkd(os.path.join(''.join(localdir[0].split(self.localpath)),subdirs).replace(os.sep,'/'))
		        except ftplib.error_perm:
			    pass
			
	for localdir in os.walk(self.localpath):
	    for files in os.listdir(localdir[0]):
	        if os.path.isfile(os.path.join(localdir[0],files)):
		    with open(os.path.join(localdir[0],files),'rb') as subfile:
		        try:
		            ftps.storbinary('STOR %s' % (os.path.join(''.join(localdir[0].split(self.localpath)),files).replace(os.sep,'/')),subfile,bufsize)
		            #print os.path.join(''.join(localdir[0].split(self.localpath)),files).replace(os.sep,'/')
			except ftplib.error_perm:
			    pass
	ftps.quit()

if __name__ == '__main__':
    myftp = Myftp('username','password','localpath','ftp_server_ip')
    myftp.loadfile()
