#!/usr/bin/env python
import time
import sys
from os import popen
import WiiInput

def write(str):
	sys.stdout.write(str)

WiiInput.startInputThread()

write("\x1b[?25l\f")
sys.stdout.flush()

height, width = popen('stty size','r').read().split()

try:
	while 1:
		pressed = ""
		for Button, Value in WiiInput.buttons.items():
			if Value == True:
				pressed += ", "+Button
		x = str(WiiInput.IR['x']*int(width)/1000)
		y = str(WiiInput.IR['y']*int(height)/1000)

		#write("\x1b[H\x1b[K"+pressed[2:]+"\n")
		write("\b \x1b["+y+";"+x+"H"+WiiInput.IR['Cursor'])
		sys.stdout.flush()
		time.sleep(.01)
except KeyboardInterrupt:
	WiiInput.die = True
	write("\fGoodbye!\n\x1b[?25h")
	sys.stdout.flush()
	sys.exit(0)
	sys.exit(0)
