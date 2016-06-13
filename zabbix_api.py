#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

class Zabbix_api:
    def __init__(self,user,passwd,apiurl):
        self.url = apiurl
	self.urls = 'http://test.ip138.com/query/'
	self.headers = {'Content-Type':'application/json'}
	self.data = {
    		"jsonrpc":"2.0",
    		"method":"user.login",
    		"params":{
        	    "user":user,
        	    "password":passwd
    		},
    		"id":1,
	    }
    def localip(self):
	try:
            get_ip = requests.get(self.urls)
	except Exception as e:
	    print Exception,':',e
	else:
	    if get_ip.status_code == requests.codes.ok:
	        local_ip = json.loads(get_ip.content)['ip']
	return str(local_ip)
        
    def get_auth(self):
	try:
            info = requests.post(self.url,data=json.dumps(self.data),headers=self.headers)
	except Exception as e:
	    print Exception,":",e
	else:
	    if info.status_code == requests.codes.ok:
	        reponse = json.loads(info.content)
	        if reponse.has_key('error'):
	            print reponse['error']['message']
	        else:
	            auth = reponse['result']
	    else:
	        print info.raise_for_status()
	return auth
	        
    def get_host(self):
	auths = self.get_auth()
	hlist = []
	get_host = {
               "jsonrpc": "2.0",
               "method": "hostgroup.get",
               "params": {
                   "output": "extend",
                       "filter": {
                            "groupid": "53"
                       },
	           "selectHosts" : ["host"]
                },
                "auth": auths,
                "id": 1
            }
	try:
            host_request = requests.post(self.url,data=json.dumps(get_host),headers=self.headers)
	except Exception as e:
	    print Exception,':',e
	else:
	    if host_request.status_code == requests.codes.ok:
                for i in json.loads(host_request.content)['result'][0]['hosts']:
	            hlist.append(i['host'])
	if hlist:
            return hlist
	else:
	    print 'The list is empty'
 
    def add_host(self):
	auths = self.get_auth()
	all_host = self.get_host()
	new_host = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": self.localip(),
		"name": "奇迹MU-" + self.localip(),
                "interfaces": [
                   {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": self.localip(),
                    "dns": "",
                    "port": "10050"
                   }
                ],
               "groups": [
                    {
                    "groupid": "53"
                    }
               ],
               "templates": [
                    {
                   "templateid": "11226"
                   },
	           {
		   "templateid": "10700"
		   },
		   {
		   "templateid": "10105"
		   }
               ],
              "inventory_mode": 0,
            },
        "auth": auths,
        "id": 1
      }
	
	if self.localip() not in all_host:
	    try:
	        host_request = requests.post(self.url,data=json.dumps(new_host),headers=self.headers)
	    except Exception as e:
	        print Exception,':',e
	    else:
		print 'Success..'


if __name__ == '__main__':
    web_add = Zabbix_api('user','passwd','zabbix_api_url')
    web_add.add_host()
