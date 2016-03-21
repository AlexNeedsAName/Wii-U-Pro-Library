import sys
import threading
from collections import OrderedDict

#Accelerometer:	/dev/event0
#IR:		/dev/event1
#Buttons:	/dev/event2

AccelerometerIn = open('/dev/input/event0','r')
IRIn = open('/dev/input/event1','r')
ButtonsIn = open('/dev/input/event2','r')

#TODO: Accelerometer Support
IR = { 'x1':-1, 'y1':-1 } #Values are roughly 0-1020 for x and 0-760 for y. -1 is out of bounds
buttons = OrderedDict([('A', False), ('B', False), ('1', False), ('2', False), ('Up', False), ('Down', False), ('Left', False), ('Right', False),  ('-', False), ('+', False), ('Home', False)])

def startInputThread():
	ButtonThread = threading.Thread(target=runButton, args=())
	ButtonThread.setDaemon(True)
	ButtonThread.start()

	IRThread = threading.Thread(target=runIR, args=())
	IRThread.setDaemon(True)
	IRThread.start()

	
def runIR():
	while 1:
		data = IRIn.read(16).encode("hex").upper()
		array = [data[i:i+4] for i in range(0, len(data), 4)]
		if(array[4] == '0300'): #It's IR (Not just null data)
			if(array[6] != 'FF03'):
				if(array[5] == '1000' or array[5] == '1200'): #X-Axis
					IR['x'] = 1015-int(array[6][2:]+array[6][:2], 16)

				elif(array[5] == '1100' or array[5] == '1300'): #Y-Axis
					IR['y'] = int(array[6][2:]+array[6][:2], 16)
			else:
				IR['x'] = -1
				IR['y'] = -1

def runButton():
	while 1:
		data = ButtonsIn.read(16).encode("hex").upper()
		array = [data[i:i+4] for i in range(0, len(data), 4)]
		if(array[4] == '0100'): #Button Press
			state = False
			if(array[6] == '0100'):
				state = True
			elif(array[6] == '0000'):
				state = False

			#D-Pad:
			if(array[5]=='6700'):
				buttons['Up'] = state
			elif(array[5]=='6C00'):
				buttons['Down'] = state
			elif(array[5]=='6900'):
				buttons['Left'] = state
			elif(array[5]=='6A00'):
				buttons['Right'] = state
			#A B 1 2
			elif(array[5]=='3001'):
				buttons['A'] = state
			elif(array[5]=='3101'):
				buttons['B'] = state
			elif(array[5]=='0101'):
				buttons['1'] = state
			elif(array[5]=='0201'):
				buttons['2'] = state
			#- Home +
			elif(array[5]=='9C01'):
				buttons['-'] = state
			elif(array[5]=='9701'):
				buttons['+'] = state
			elif(array[5]=='3C01'):
				buttons['Home'] = state
