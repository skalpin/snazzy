import assemble
import util
import camera
import os
from os.path import join
import time

width = 2080
height = 1920
PAUSE_MAX = 3
takes = 3

def run():
	camera.warmup(width, height)
	images = []
	for i in range(takes):			
		pic_paths = camera.take(1, width, height)
		start = time.time()
		image1 = util.process(pic_paths[0], assemble.get_height_each())
		end = time.time()
		diff = end - start
		images.append(image1)
		print "took in: " + str(diff) + "ms"
		if(diff < PAUSE_MAX and i < takes - 1):
			sleep_time = PAUSE_MAX - diff
			print "sleeping for another: " + str(sleep_time) + "ms"
			time.sleep(diff)

	assemble.assemble(images)

run()
