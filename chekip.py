#!/usr/bin/python
import requests
import sys
import socket
import re

lists = ['ip','country','region','city','isp']

def _chek_ip():
    params = {'ip':params_one}
    url = 'http://ip.taobao.com/service/getIpInfo.php'
    request = requests.get(url,params=params)
    if request.status_code == requests.codes.ok:
        response = request.json()['data']
        try:
            for i in lists:
	        print response[i],
	except:
	    pass

if __name__ == '__main__':
    matching = re.compile('^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$')
    try:
        params_one = sys.argv[1]
	params_one
    except IndexError:
        print 'Params > 1 = 1 or null...'
    else:
        try:
	    socket.inet_aton(params_one)
	except socket.error:
	    print 'Ip:%s address error..' % params_one
	    print 2
	else:
	    if matching.match(params_one) == None:
 		print 'Ip:%s address error..' % params_one
		print 1
	    else:
		_chek_ip()
