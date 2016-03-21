#!/usr/bin/env python
import time
import sys
import WiiInput

def write(str):
	sys.stdout.write(str)

WiiInput.startInputThread()

write("\x1b[?25l\f\nx:\ny:")
sys.stdout.flush()

try:
	while 1:
		pressed = ""
		for Button, Value in WiiInput.buttons.items():
			if Value == True:
				pressed += ", "+Button
		write("\x1b[H\x1b[K"+pressed[2:]+"\n")
		write("\x1b[2;4H\x1b[K"+str(WiiInput.IR['x']))
		write("\x1b[3;4H\x1b[K"+str(WiiInput.IR['y']))
		sys.stdout.flush()
		time.sleep(.1)
except KeyboardInterrupt:
	write("\fGoodbye!\n\x1b[?25h")
	sys.stdout.flush()
	sys.exit(0)
