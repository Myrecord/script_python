#!/usr/bin/python

import os
import time
import tarfile

def Backup_log(Source_Dir,Dest_Dir):
    Refile = 15 // 删除15天前的备份文件
    Date = time.strftime('%Y%m%d')
    File_type = os.path.isfile
    if os.path.isdir(Source_Dir):
        if os.path.exists(Dest_Dir):
	    Dir_list = os.listdir(Source_Dir)
            Bale = tarfile.open(Dest_Dir +'/'+ Date +'.tar.gz','w:gz')
	    for i in Dir_list:
		fullpath = os.path.join(Source_Dir+'/',i)
	        Bale.add(fullpath,arcname=i)
	    Bale.close()
	    for Path,Name,Log in os.walk(Source_Dir):
                for Files in Log:
	            os.remove(os.path.join(Path,Files))
	    for j in os.listdir(Dest_Dir):
		Filename = os.path.basename(j).split('.')[0]
	        Days = int(Date) - int(Filename)
		if Days >= Refile:
		    os.remove(Dest_Dir + '/' + j)
	else:
	    os.makedirs(Dest_Dir)
if __name__ == "__main__":
    Backup_log('/tmp','/data/backup')
