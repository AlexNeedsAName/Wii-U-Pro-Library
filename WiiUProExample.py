#!/usr/bin/env python
import time
import sys
import WiiUProInput

def write(str):
	sys.stdout.write(str)

WiiUProInput.startInputThread()

write("\x1b[?25l\f\nLeft X:  0\nLeft Y:  0\nRight X: 0\nRight Y: 0")
sys.stdout.flush()

try:
	while 1:
		pressed = ""
		for Button, Value in WiiUProInput.buttons.items():
			if Value == True:
				pressed += ", "+Button
		write("\x1b[H\x1b[K"+pressed[2:])
		write("\x1b[2;10H\x1b[K"+str(WiiUProInput.axes["LeftX"]))
		write("\x1b[3;10H\x1b[K"+str(WiiUProInput.axes["LeftY"]))
		write("\x1b[4;10H\x1b[K"+str(WiiUProInput.axes["RightX"]))
		write("\x1b[5;10H\x1b[K"+str(WiiUProInput.axes["RightY"]))
		sys.stdout.flush()
		time.sleep(.1)
except KeyboardInterrupt:
		write("\fGoodbye!\n\x1b[?25h")
		sys.stdout.flush()
		sys.exit(0)
