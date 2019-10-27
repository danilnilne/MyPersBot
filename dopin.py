import RPi.GPIO as GPIO

from time import sleep

GPIO.setwarnings(False)
 
GPIO.setmode(GPIO.BCM)

channels_used = [5, 13, 27]

for channel in channels_used:

	GPIO.setup(channel, GPIO.OUT);

	GPIO.output(channel, True)

	sleep(2)


for channel in channels_used:

	GPIO.cleanup(channel);
