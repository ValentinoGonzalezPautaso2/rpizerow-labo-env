from gpiozero import LED, Buzzer
from time import sleep

red = LED(19)
green = LED (13)
blue = LED (26)
buzz = Buzzer (22)


def rgb_red():
	global red
	red.toggle()

def rgb_blue():
	global blue
	blue.toggle()

def rgb_green():
	global green
	green.toggle()

def buzzer(state):
	global buzz
	if state == "on":
		buzz.on()
	elif state == "off":
		buzz.off()

comps = {
	"rgb red": rgb_red,
	"rgb blue": rgb_blue,
	"rgb green": rgb_green,
	"buzzer": buzzer
}


while True:

	comando = input("prompt: ")

	if comando in comps:

		comps[comando]()

