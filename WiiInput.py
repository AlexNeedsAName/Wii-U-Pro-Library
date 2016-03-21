import sys
import threading
from collections import OrderedDict
from math import atan	#Trig!
from math import degrees

#Accelerometer:	/dev/event0
#IR:		/dev/event1
#Buttons:	/dev/event2

AccelerometerIn = open('/dev/input/event0','r')
IRIn = open('/dev/input/event1','r')
ButtonsIn = open('/dev/input/event2','r')

#TODO: Accelerometer Support
IR = { 'x1':0, 'y1':0, '1on':False, 'x2':0, 'y2':0, '2on':False, 'Angle':0 } #Values are roughly 0-1020 for x and 0-760 for y.
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
			cord = ''
			on = False
			if(array[5] == '1000'):
				cord = 'x1'
			elif(array[5] == '1100'):
				cord = 'y1'
			elif(array[5] == '1200'):
				cord = 'x2'
			elif(array[5] == '1300'):
				cord = 'y2'
			if(cord != ''):
				if(array[6] != 'FF03'):
					if('x' in cord):
						IR[cord] = 1016-int(array[6][2:]+array[6][:2], 16)
					else:
						IR[cord] = int(array[6][2:]+array[6][:2], 16)
					on = True
			if('1' in cord):
				IR['1on'] = on
			elif('2' in cord):
				IR['2on'] = on
			
			#Angle Calculations
			#Start with the weird cases
			if(not IR['1on'] or not IR['2on']): #Only one/none is detected
				IR['Angle'] = 0
			elif(IR['x1'] == IR['x2']):
				if(IR['y1'] < IR['y2']):
					IR['Angle'] = 90
				else:
					IR['Angle'] = 270
			elif(IR['y1'] == IR['y2']): 
				if(IR['x1'] < IR['x2']):
					IR['Angle'] = 180
				else:
					IR['Angle'] = 0
			#Now for the majorty of the time
			else: #HashtagTrigTime
				rise = float(IR['y1'] - IR['y2'])
				run = float(IR['x1'] - IR['x2'])
				
				angle = degrees(atan(abs(rise/run)))
				if(rise > 0):
					if(run > 0):
						IR['Angle'] = 270+(90-angle)
					else:
						IR['Angle'] = 180+angle
				else:
					if(run > 0):
						IR['Angle'] = 0+angle
					else:
						IR['Angle'] = 90+(90-angle)

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
