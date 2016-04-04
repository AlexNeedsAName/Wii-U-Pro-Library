import sys
import threading
from collections import OrderedDict
from math import atan	#Trig!
from math import degrees

#Accelerometer:	/dev/input/event0
#IR:		/dev/input/event1
#Buttons:	/dev/input/event2
#Accessory: 	/dev/input/event3
	
#TODO: Accelerometer Support
#TODO: IR Rotation of plane to match rotation

fileOffset = 1

IR = { 'x1': 0, 'y1': 0, '1on': False, 'x2': 0, 'y2': 0, '2on': False, 'Angle': 0, 'Cursor': '|', 'x': 0, 'y': 0 } #Values are 0-1000 for x and y.
buttons = OrderedDict([('A', False), ('B', False), ('C', False), ('X', False), ('Y', False), ('Z', False), ('L', False), ('R', False), ('Z', False), ('ZL', False), ('ZR', False), ('1', False), ('2', False), ('Up', False), ('Down', False), ('Left', False), ('Right', False),  ('-', False), ('+', False), ('Home', False)])
sticks = { 'lx': 0, 'rx': 0, 'nx': 0, 'ly': 0, 'ry': 0, 'ny': 0 }
ext = False

def readFrom(input):
	data = input.read(16).encode("hex").upper()
	return [data[i+2:i+4]+data[i:i+2] for i in range(0, len(data), 4)]

def start():
	Thread1 = threading.Thread(target=run, args=["/dev/input/event"+str(2+fileOffset), False, False]) #Buttons
	Thread1.setDaemon(True)
	Thread1.start()

	Thread2 = threading.Thread(target=run, args=["/dev/input/event"+str(1+fileOffset), True, False]) #IR
	Thread2.setDaemon(True)
	Thread2.start()

	Thread3 = threading.Thread(target=run, args=["/dev/input/event"+str(3+fileOffset), False, True]) #Extension
	Thread3.setDaemon(True)
	Thread3.start()

def processData(array, isIR):
	global buttons
	global sticks
	global IR

	if(not isIR):
		#Button Press
		if(array[4] == '0001'):
			if(array[6] == '0001'):
				state = True
			else:
				state = False	

			#D-Pad:
			if(array[5]=='0067'):
					buttons['Up'] = state
			elif(array[5]=='006C'):
					buttons['Down'] = state
			elif(array[5]=='0069'):
				buttons['Left'] = state
			elif(array[5]=='006A'):
				buttons['Right'] = state

			#1 2
			elif(array[5]=='0101'):
				buttons['1'] = state
			elif(array[5]=='0102'):
				buttons['2'] = state

			#A B C
			elif(array[5]=='0130'):
				buttons['A'] = state
			elif(array[5]=='0131'):
				buttons['B'] = state
			elif(array[5]=='0132'):
				buttons['C'] = state

			#X Y Z
			elif(array[5]=='0133'):
				buttons['Y'] = state
			elif(array[5]=='0134'):
				buttons['X'] = state
			elif(array[5]=='0135'):
				buttons['Z'] = state

			#L R ZL ZR
			elif(array[5]=='0136'):
				buttons['L'] = state
			elif(array[5]=='0137'):
				buttons['R'] = state
			elif(array[5]=='0138'):
				buttons['ZL'] = state
			elif(array[5]=='0139'):
				buttons['ZR'] = state

			#- Home +
			elif(array[5]=='019C'):
				buttons['-'] = state
			elif(array[5]=='0197'):
				buttons['+'] = state
			elif(array[5]=='013C'):
				buttons['Home'] = state

		#Joysticks
		elif(array[4] == '0003'):

			if(array[7] == 'FFFF'):
				flip = -65536
			else:
				flip = 0

			#Nunchuck
			if(array[5] == '0010'): 
				sticks['nx'] = int(array[6], 16) + flip
			elif(array[5] == '0011'):
				sticks['ny'] = int(array[6], 16) + flip

			#Left Stick (Game Cube Extension)
			elif(array[5] == '0012'): 
				sticks['lx'] = (int(array[6], 16) + flip) * 100 / 32
			elif(array[5] == '0013'):
				sticks['ly'] = (int(array[6], 16) + flip) * 100 / 32

			#Right Stick (Game Cube Extension)
			elif(array[5] == '0014'): 
				sticks['rx'] = (int(array[6], 16) + flip) * 100 / 32
			elif(array[5] == '0015'):
				sticks['ry'] = (int(array[6], 16) + flip) * 100 / 32
	else:
		if(array[4] == '0003'): #It's IR (Not just null data)
			cord = ''
			on = False
			if(array[5] == '0010'):
				cord = 'x1'
			elif(array[5] == '0011'):
				cord = 'y1'
			elif(array[5] == '0012'):
				cord = 'x2'
			elif(array[5] == '0013'):
				cord = 'y2'
			if(cord != ''):
				if(array[6] != '03FF'):
					if('x' in cord):
						IR[cord] = 1015-int(array[6], 16)
					else:
						IR[cord] = int(array[6], 16)
					on = True
			if('1' in cord):
				IR['1on'] = on
			elif('2' in cord):
				IR['2on'] = on
			IR['x'] = int((float(1000)/1015) * (IR['x1']+IR['x2'])/2)
			IR['y'] = int((float(1000)/760) * (IR['y1']+IR['y2'])/2)
			
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
				IR['Angle'] = round(IR['Angle'])
				
			if( 338 < IR['Angle'] <= 360 or 0 < IR['Angle'] <= 23 ):
				IR['Cursor'] = '|'
			if( 23  < IR['Angle'] <= 68  ):
				IR['Cursor'] = '/'
			if( 68  < IR['Angle'] <= 113 ):
				IR['Cursor'] = '-'
			if( 113 < IR['Angle'] <= 158 ):
				IR['Cursor'] = '\\'
			if( 158 < IR['Angle'] <= 203 ):
				IR['Cursor'] = '|'
			if( 203 < IR['Angle'] <= 248 ):
				IR['Cursor'] = '/'
			if( 248 < IR['Angle'] <= 293 ):
				IR['Cursor'] = '-'
			if( 293 < IR['Angle'] <= 338 ):
				IR['Cursor'] = '\\'
def run(path, IR, Accessory):
	file = None
	global ext
	while 1:
		try:
			if(file == None):
				file = open(path,'r')
				if(Accessory):
					ext = True
			processData(readFrom(file), IR)
		except:
			file = None
			if(Accessory):
				ext = None
				buttons['C']=buttons['Z']=buttons['L']=buttons['R']=buttons['ZL']=buttons['ZR']=buttons['X']=buttons['Y']=False
				sticks['lx']=sticks['rx']=sticks['ly']=sticks['ry']=0
start()
