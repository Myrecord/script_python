#!/usr/bin/python
#-*- coding: UTF-8 -*-

import requests
import json
import re

class TQYB:
    def __init__(self):
        self.url = 'http://tq.360.cn/api/weatherquery/querys?app=tq360&code=101010100&_jsonp=renderData'
	self.math = re.compile(r'renderData\((.*)\)')
        self.request = requests.get(self.url)
    
    def _Pm25(self):
	valuse = json.loads(self.math.findall(self.request.content)[0])['pm25']
	print  'Pm25: %d %s %s' % (valuse['aqi'],valuse['quality'],valuse['advice'])
    
    def weather(self):
	if self.request.status_code == requests.codes.ok:
	    weather_list = json.loads(self.math.findall(self.request.content)[0])['weather'][0:2]
	    Time = weather_list[0]['date']
	    weater_day = weather_list[0]['info']['day'][1]
	    day_wind = weather_list[0]['info']['day'][3:5]
	    today_night = weather_list[0]['info']['night'][2]
	    today_day =  weather_list[0]['info']['day'][2]
	    print '%s:\n%s %s~%s %s' %(Time,weater_day,today_night,today_day,''.join(day_wind))
	    self._Pm25()

if __name__ == '__main__':
 tianqi = TQYB()
 tianqi.weather()
