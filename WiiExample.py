#!/usr/bin/env python
import time
import sys
import WiiInput

def write(str):
	sys.stdout.write(str)

WiiInput.startInputThread()

write("\x1b[?25l\f\nx1:\ny1:\nOn:\nx2:\ny2:\nOn:\nAngle:")
sys.stdout.flush()

try:
	while 1:
		pressed = ""
		for Button, Value in WiiInput.buttons.items():
			if Value == True:
				pressed += ", "+Button
		write("\x1b[H\x1b[K"+pressed[2:]+"\n")
		write("\x1b[2;5H\x1b[K"+str(WiiInput.IR['x1']))
		write("\x1b[3;5H\x1b[K"+str(WiiInput.IR['y1']))
		write("\x1b[4;5H\x1b[K"+str(WiiInput.IR['1on']))
		write("\x1b[5;5H\x1b[K"+str(WiiInput.IR['x2']))
		write("\x1b[6;5H\x1b[K"+str(WiiInput.IR['y2']))
		write("\x1b[7;5H\x1b[K"+str(WiiInput.IR['2on']))
		write("\x1b[8;8H\x1b[K"+str(WiiInput.IR['Angle']))
		sys.stdout.flush()
		time.sleep(.1)
except KeyboardInterrupt:
	write("\fGoodbye!\n\x1b[?25h")
	sys.stdout.flush()
	sys.exit(0)
