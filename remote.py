#/usr/bin/python
# -*- coding: utf8 -*-

import os,sys
import time
import re
import xlrd
from termcolor import colored
import threading
from paramiko import SSHClient
from paramiko import AutoAddPolicy,RSAKey
from cmd import Cmd

class remote(SSHClient):
    def __init__(self):
        SSHClient.__init__(self)
	self.login_status = None

    def ssh_connect(self,host,passwd,port=22,user='root',key=None,key_pass=None):
        self.set_missing_host_key_policy(AutoAddPolicy())
    	if key:
	    try:
	        key_file = RSAKey.from_private_key_file(key)
	    except PasswordRequiredException:
		key_file = RSAkey.from_private_key_file(key,key_pass)
	else:
	    key_file = None
	try:
	    self.connect(host,port=port,username=user,password=passwd,pkey=key_file,timeout=3)
	    self.login_status = True
	except Exception,ex:
	    print host,colored(ex,'red',attrs=['bold'])
	    self.login_status = False

    def ssh_command(self,command):
        if self.login_status:
	    stdin,stdout,stderr = self.exec_command(command)
	    output = stdout.read().strip('\n')
	    error = stderr.read().strip('\n')
	    if output:
	        return output
	    else:
		return error
	    
    def put_ftp(self,loadpath,remotepath):
        if self.login_status:
	    client = self.open_sftp()
	    try:
	        client.put(loadpath,remotepath)
		return True
	    except Exception,ex:
		return ex

class client_main(Cmd):
    def __init__(self,password,filepath):
	Cmd.__init__(self)
	self.prompt = 'root#>'
	self.session = {}
	self.host = []
	self.password = password
	self.connect_number = []
	self.filepath = filepath
	self.lists = []

    def do_connect(self,args):
	host_number = 0
	matching = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
	if 'connect' not in self.connect_number:
	    try:
	        data = xlrd.open_workbook(self.filepath)
	    except IOError,e:
		print colored('No such excel file.','red',attrs=['bold'])
		sys.exit()
	    table = data.sheet_by_index(1)
	    for i in range(table.nrows):
		self.lists.append('-'.join(table.row_values(i)[:2]))

	    start = time.time()
	    for i in self.lists:
		if matching.match(i.split('-')[1]):
		    self.host.append(i)
                    host_session = remote()
		    t = threading.Thread(target=host_session.ssh_connect,args=(i.split('-')[1],self.password))
		    t.start()
		    self.session[i.split('-')[1]] = host_session
		    host_number += 1
		else:
		    print colored('Ip address: %s error' % i.strip('-')[1],'magenta',attrs=['bold'])
	    end = time.time()
	    self.connect_number.append('connect')
	    print colored('\nConnect host number %s,Time:' % (host_number),'green',attrs=['bold']),colored(str(end - start) + 's','magenta',attrs=['bold'])
	
    def do_cmd(self,args):
	localtime = str(time.strftime("%Y-%m-%d %T"))
	with open('/var/log/log.txt','a+') as files:
	    files.write('[%s %s]:' %(localtime,self.prompt) + args + '\n')
	for i in self.host:
	    print colored('[%s]:\n\n' % i,'yellow',attrs=['bold']),self.session[i.split('-')[1]].ssh_command(args) + '\n'

    def do_ls(self,args):
	os.system('ls %s' % args)
	
    def do_put(self,args):
	args = args.split()
	if len(args) == 2:
	    for i in self.host:
	       print colored('[%s]:\n\n' % i,'yellow',attrs=['bold']),self.session[i.split('-')[1]].put_ftp(args[0],args[1])
	else:
	    print colored('Error,Input (loadpath remotepath)','red',attrs=['bold'])
    
    def do_show_host(self,args):
	print self.host
    
    def do_exit(self,args):
	exit(1)
   
if __name__ == '__main__':
    runs = client_main('password','xlsx_file')
    runs.cmdloop()
