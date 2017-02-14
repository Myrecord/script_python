#!/usr/bin/python
# -*- coding: utf8 -*-
import os,sys
import time
import re
from termcolor import cprint
from threading import Thread
from paramiko import SSHClient
from paramiko import AutoAddPolicy,RSAKey
from cmd import Cmd

results = []

echo_info = lambda x:cprint(x,'yellow',attrs=['bold'])
error = lambda x:cprint(x,'magenta',attrs=['bold'])

def tasks(args,session,i):
    args = args.split()
    echo_info('[%s]:\n\n' % i.strip('\n') + str(session[i].put_ftp(args[0],args[1])))

class remote(SSHClient):
    def __init__(self):
        SSHClient.__init__(self)
	self.login_status = None

    def ssh_connect(self,host,passwd,port=22,user='root',key=None,key_pass=None,timeout=3):
        self.set_missing_host_key_policy(AutoAddPolicy())
    	if key:
	    try:
	        key_file = RSAKey.from_private_key_file(key)
	    except PasswordRequiredException:
		key_file = RSAkey.from_private_key_file(key,key_pass)
	else:
	    key_file = None
	try:
	    self.connect(host,port=port,username=user,password=passwd,pkey=key_file,timeout=2)
	    self.login_status = True
	except:
	    error(host+':connect failure')
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
	        with open(self.filepath) as files:
		    for i in files.readlines():
		        self.lists.append(i)
	    except (IOError,IndexError):
		error('Open file failure,check file format.')
		sys.exit()

	    start = time.time()
	    for i in self.lists:
		if matching.match(i):
                    host_session = remote()
		    t = Thread(target=host_session.ssh_connect,args=(i.strip('\n'),self.password))
		    results.append(t)
		    t.start()
		    for connect_task in results:
		        connect_task.join()
		    if host_session.login_status:
		        self.host.append(i)
		        self.session[i] = host_session
		        host_number += 1
		else:
		    error('Ip address: %s error' % i)
	    end = time.time()
	    self.connect_number.append('connect')
	    echo_info('Connect host number %s,Time:' % host_number + (str(end - start) + 's'))
	
    def do_cmd(self,cmds):
	localtime = str(time.strftime("%Y-%m-%d %T"))
	with open('/var/log/log.txt','a+') as files:
	    files.write('[%s %s]:' %(localtime,self.prompt) + cmds + '\n')
	for i in self.host:
	    echo_info('[%s]:\n'%i.strip('\n'))
	    print self.session[i].ssh_command(cmds)

    def do_ls(self,args):
	os.system('ls %s' % args)
	
    def do_put(self,args):
	for i in self.host:
	    t = Thread(target=tasks,args=(args,self.session,i,))
	    results.append(t)
	    t.start()
        for taks in results:
	    taks.join()
    
    def do_show_host(self,args):
	for i in self.host:
	    print i
    
    def do_exit(self,args):
	exit(1)

   
if __name__ == '__main__':
    runs = client_main('12ZteLwNopwlQ','/usr/local/sbin/a')
    runs.cmdloop()
