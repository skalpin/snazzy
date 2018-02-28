#!/usr/bin/env python

import os
import time

def measure_temp():
	temp = os.popen("vcgencmd measure_temp").readline()
	return temp.replace('\r', "").replace('\n', "").replace("temp=","")

while True:
	print('\r' + measure_temp(), end="\r", flush=True)
	time.sleep(.1)
