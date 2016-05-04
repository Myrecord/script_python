#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import time
import tarfile
import MySQLdb

Date = time.strftime('%Y%m%d')
set_time = 4 //删除4天前备份的数据

class Backup_Sql:
    def __init__(self,Host,User,Passwd,Backdir):
        self.host = Host
	self.user = User
	self.passwd = Passwd
	self.backdir = Backdir
    def Sql_file(self):
	    f = open('/usr/local/sbin/error_db.log','a')
            try:
                Connect = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,connect_timeout=1)
    	    except MySQLdb.OperationalError, e:
		f.write(Date + ':' + e[1] + '\n')
    	        sys.exit()
    	    else:
    	        Mysql = Connect.cursor()
    	        All_db = Mysql.execute("show databases;")
    	        result = Mysql.fetchall()
	    f.close()
    	    Mysql.close()
    	    Connect.close()
    	    return result
    def Tar_file(self):
        Info = self.Sql_file()
	bashfile = open('/data/start.sh')
	string = re.findall(r'-db_name=\"(.*?)\"',bashfile.read())[0]
	names = Info[Info.index((string,))][0]
        if not os.path.exists(self.backdir):
            os.mkdir(self.backdir)
	else:
	    os.system('/usr/bin/mysqldump --default-character-set=utf8 -u%s -p%s -h%s %s >> %s/%s.sql' % (self.user,self.passwd,self.host,names,self.backdir,names))
	    Bale = tarfile.open(self.backdir +'/'+ Date + '-' + names +'.tar.gz','w:gz') 
	for file in os.listdir(self.backdir):
	    if file.endswith('sql'):
	        fullpath = os.path.join(self.backdir+'/',file)
	        Bale.add(fullpath,arcname=file)
		os.remove(fullpath)
	Bale.close()
	for dirpath,dirs,File in os.walk(self.backdir):
	    for Files in File:
		Sou_file = os.path.join(dirpath,Files)
		Ctime = os.stat(Sou_file)
		Ctimes = time.strftime('%Y%m%d',time.gmtime(Ctime.st_ctime))
		Dates = int(Date) - int(Ctimes)
		if Dates >= set_time:
		    os.remove(Sou_file)
def Set_Name():
    New_name = Backup_Sql('db_address','user','passwd,'target_backup_dir')
    New_name.Tar_file()

if __name__ == "__main__" :
    Set_Name()
 
