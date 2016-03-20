import sys
from collections import OrderedDict

pipe = open('/dev/input/event0','r')
data = ''
array = []
buttons = OrderedDict([('A', False), ('B', False), ('X', False), ('Y', False), ('Up', False), ('Down', False), ('Left', False), ('Right', False),  ('Select', False), ('Start', False), ('Home', False), ('LS', False), ('RS', False), ('L', False), ('R', False), ('ZL', False), ('ZR', False)])
axes = {'LeftX': 0, 'LeftY': 0, 'RightX': 0, 'RightY': 0}

def runInputThread():
	while 1:
		data = pipe.read(16).encode("hex").upper()
		array = [data[i:i+4] for i in range(0, len(data), 4)]
		if(array[4] == '0100'): #Button Press
			state = False
			if(array[6] == '0100'):
				state = True
			elif(array[6] == '0000'):
				state = False
	
			#D-Pad:
			if(array[5]=='2002'):
				buttons['Up'] = state
			elif(array[5]=='2102'):
				buttons['Down'] = state
			elif(array[5]=='2202'):
				buttons['Left'] = state
			elif(array[5]=='2302'):
				buttons['Right'] = state
			#A B X Y
			elif(array[5]=='3001'):
				buttons['B'] = state
			elif(array[5]=='3101'):
				buttons['A'] = state
			elif(array[5]=='3301'):
				buttons['X'] = state
			elif(array[5]=='3401'):
				buttons['Y'] = state
			#Triggers
			elif(array[5]=='3601'):
				buttons['L'] = state
			elif(array[5]=='3701'):
				buttons['R'] = state
			elif(array[5]=='3801'):
				buttons['ZL'] = state
			elif(array[5]=='3901'):
				buttons['ZR'] = state
			#Select Home Start
			elif(array[5]=='3A01'):
				buttons['Select'] = state
			elif(array[5]=='3B01'):
				buttons['Start'] = state
			elif(array[5]=='3C01'):
				buttons['Home'] = state
			#Stick Button
			elif(array[5]=='3D01'):
				buttons['LS'] = state
			elif(array[5]=='3E01'):
				buttons['RS'] = state
				
		elif(array[4] == '0300'): #It's a joystick!
			num = int(array[6][2:]+array[6][:-2], 16) #Take the first byte and put it after the second byte. Because that's a logical way to send the data. Pffft.
			if(array[7] == 'FFFF'):
				num = num - 65536
			percent = num/10
			if(percent>100):
				percent = 100
			if(percent<-100):
				percent =-100
			#num=num*100/1225
						
			if(array[5] == '0000'): #Which one though?
				axes['LeftX'] = percent
			elif(array[5] == '0100'):
				axes['LeftY'] = -percent
			if(array[5] == '0300'):
				axes['RightX'] = percent
			elif(array[5] == '0400'):
				axes['RightY'] = -percent
