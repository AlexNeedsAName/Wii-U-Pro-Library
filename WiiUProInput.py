import sys
import threading
from collections import OrderedDict

buttons = OrderedDict([('A', False), ('B', False), ('X', False), ('Y', False), ('Up', False), ('Down', False), ('Left', False), ('Right', False),  ('Select', False), ('Start', False), ('Home', False), ('LS', False), ('RS', False), ('L', False), ('R', False), ('ZL', False), ('ZR', False)])
axes = {'LeftX': 0, 'LeftY': 0, 'RightX': 0, 'RightY': 0}

def start():
	InputThread = threading.Thread(target=runInput, args=())
	InputThread.setDaemon(True)
	InputThread.start()

def readFrom(input):
	data = input.read(16).encode("hex").upper()
	return [data[i+2:i+4]+data[i:i+2] for i in range(0, len(data), 4)]

def runInput():
	pipe = open('/dev/input/event0','r')
	while 1:
		try:
			if(pipe == None):
				pipe = open('/dev/input/event0','r')
			array = readFrom(pipe)
			if(array[4] == '0001'): #Button Press
				state = False
				if(array[6] == '0001'):
					state = True
				elif(array[6] == '0000'):
					state = False
		
				#D-Pad:
				if(array[5]=='0220'):
					buttons['Up'] = state
				elif(array[5]=='0221'):
					buttons['Down'] = state
				elif(array[5]=='0222'):
					buttons['Left'] = state
				elif(array[5]=='0223'):
					buttons['Right'] = state
				#A B X Y
				elif(array[5]=='0130'):
					buttons['B'] = state
				elif(array[5]=='0131'):
					buttons['A'] = state
				elif(array[5]=='0133'):
					buttons['X'] = state
				elif(array[5]=='0134'):
					buttons['Y'] = state
				#Triggers
				elif(array[5]=='0136'):
					buttons['L'] = state
				elif(array[5]=='0137'):
					buttons['R'] = state
				elif(array[5]=='0138'):
					buttons['ZL'] = state
				elif(array[5]=='0139'):
					buttons['ZR'] = state
				#Select Home Start
				elif(array[5]=='013A'):
					buttons['Select'] = state
				elif(array[5]=='013B'):
					buttons['Start'] = state
				elif(array[5]=='013C'):
					buttons['Home'] = state
				#Stick Button
				elif(array[5]=='013D'):
					buttons['LS'] = state
				elif(array[5]=='013E'):
					buttons['RS'] = state
					
			elif(array[4] == '0003'): #It's a joystick!
				num = int(array[6], 16)
				if(array[7] == 'FFFF'):
					num = num - 65536
				percent = float(num)/10
				if(percent>100):
					percent = 100.0
				if(percent<-100):
					percent =-100.0
							
				if(array[5] == '0000'): #Which one though?
					axes['LeftX'] = percent
				elif(array[5] == '0001'):
					axes['LeftY'] = -percent
				if(array[5] == '0003'):
					axes['RightX'] = percent
				elif(array[5] == '0004'):
					axes['RightY'] = -percent
		except:
			pipe = None
			conn = False

start()
