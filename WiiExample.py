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

try:
	while 1:
		height, width = popen('stty size','r').read().split()
		
		pressed = ""
		for Button, Value in WiiInput.buttons.items():
			if Value == True:
				pressed += ", "+Button
		pressed = pressed[2:]
		x = str(WiiInput.accessory['stick']['x'])
		y = str(WiiInput.accessory['stick']['y'])
		
		
		write("\x1b[H\x1b[K"+pressed+"\n")
		write('Accessory: '+str(WiiInput.accessory['connected'])+' '+x+";"+y+' '+str(WiiInput.accessory['buttons']))

		sys.stdout.flush()
		time.sleep(.1)
except KeyboardInterrupt:
	write("\fGoodbye!\n\x1b[?25h")
	sys.stdout.flush()
	sys.exit(0)
