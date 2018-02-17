import threading
import time
import queue
from threading import Thread
from queue import Queue

class ActionQueue(Thread):
	def __init__(self, actor_name, delegate):
		self._actor_name = actor_name
		self._delegate = delegate
		self._queue = Queue()
		Thread.__init__(self)
		self._stop_event = threading.Event()
		self.start()

	def add(self, *args):
		self._queue.put(args)

	#Run the thread and print out messages from the queue.
	def run(self):
		while True:
			try:
				args = self._queue.get(False)
				print(self._actor_name, args)
				self._delegate(*args)
			except queue.Empty:
				if self._stop_event.is_set():
					break
				else:
					time.sleep(3)
		print(self._actor_name + " completed")

	def stop(self):
		self._stop_event.set()
