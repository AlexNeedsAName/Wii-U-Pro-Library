#!/usr/bin/env python
import time
import sys
from os import popen
import WiiInput

IR = 1
Buttons = 2
Stick = 3

TestState = IR

def write(str):
	sys.stdout.write(str)

WiiInput.start()

write("\x1b[?25l\f")

try:
	while 1:

		if(TestState == IR):
			height, width = popen('stty size','r').read().split()
		
			x=WiiInput.IR['x']*int(width)/1000
			y=WiiInput.IR['y']*int(height)/1000

			write("\b \x1b["+str(y)+";"+str(x)+"H"+WiiInput.IR['Cursor'])

		elif(TestState == Buttons):
			pressed = ""
			for Button, Value in WiiInput.buttons.items():
				if Value == True:
					pressed += ", "+Button
			pressed = pressed[2:]
		
			write("\x1b[H\x1b[K"+pressed+"\n")
		
		elif(TestState == Sticks):
			write("\x1b[H"+str(WiiInput.sticks))

		sys.stdout.flush()
		time.sleep(.1)
except KeyboardInterrupt:
	write("\fGoodbye!\n\x1b[?25h")
	sys.stdout.flush()
	sys.exit(0)
