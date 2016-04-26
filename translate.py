#!/usr/bin/python
# -*- coding:utf-8 -*-  

import requests
import sys
import hashlib
import time

lists = ['src','dst']

def main(context):
    keys_md5 = hashlib.md5()
    keys_md5.update('20160201000010368' + context + str(int(time.time())) + '_4Vs69w4f2RV5Oz1i1sH')
    params = {'q':context,'from':'auto','to':'auto','appid':'20160201000010368','salt':int(time.time()),'sign':keys_md5.hexdigest()}
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    request = requests.get(url,params=params)
    if request.status_code == requests.codes.ok:
        vlause = request.json()['trans_result'][0]
        for i in lists:
            print vlause[i],

if __name__ == '__main__':
    params_one = ' '.join(sys.argv[1:])
    if not params_one.strip():
        pass
    else:
	main(params_one)
        
