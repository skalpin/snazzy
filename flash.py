import RPi.GPIO as GPIO
from time import sleep

class Flash:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)

	def on(self):
		GPIO.output(18, True)

	def off(self):
		GPIO.output(18, False)

	def blink(self):
		GPIO.output(18, False)
		sleep(1)
		GPIO.output(18, True)
