from gpiozero import LED
from time import sleep

Rled = LED(13)
Gled = LED(19)
Bled = LED(26)

while True:
	Gled.on()
	sleep(0.25)
	Bled.off()

	Rled.on()
	sleep (1)
	Gled.off()

	Bled.on()
	sleep(0.5)
	Rled.off
