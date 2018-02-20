import threading
import time
import queue
from threading import Thread
from queue import Queue

class ResourceQueue(Thread):
	def __init__(self, actor_name, resource):
		self._actor_name = actor_name
		self._resource = resource
		self._queue = Queue()
		Thread.__init__(self)
		self._stop_event = threading.Event()
		self.start()

	def add(self, delegate):
		self._queue.put(delegate)

	#Run the thread and print out messages from the queue.
	def run(self):
		while True:
			try:
				delegate = self._queue.get(False)
				print(self._actor_name, 'executing')
				delegate(self._resource)
			except queue.Empty:
				if self._stop_event.is_set():
					break
				else:
					time.sleep(3)
		print(self._actor_name + " completed")

	def stop(self):
		self._stop_event.set()
		self.join()
