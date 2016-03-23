
import sys
import threading
from collections import OrderedDict
from math import atan	#Trig!
from math import degrees

#Accelerometer:	/dev/input/event0
#IR:		/dev/input/event1
#Buttons:	/dev/input/event2
#AccessoryL 	/dev/input/event3
	
#TODO: Accelerometer Support
#TODO: IR Rotation of plane to match rotation

IR = { 'x1': 0, 'y1': 0, '1on': False, 'x2': 0, 'y2': 0, '2on': False, 'Angle': 0, 'Cursor': '|', 'x': 0, 'y': 0 } #Values are 0-1000 for x and y.
buttons = OrderedDict([('A', False), ('B', False), ('1', False), ('2', False), ('Up', False), ('Down', False), ('Left', False), ('Right', False),  ('-', False), ('+', False), ('Home', False)])
accessory = { 'connected': None, 'buttons': {'C': False, 'Z': False }, 'stick': { 'x': 0, 'y': 0 } }

def readFrom(input):
	data = input.read(16).encode("hex").upper()
	return [data[i+2:i+4]+data[i:i+2] for i in range(0, len(data), 4)]

def startInputThread():

	ButtonThread = threading.Thread(target=runButton, args=())
	ButtonThread.setDaemon(True)
	ButtonThread.start()

	IRThread = threading.Thread(target=runIR, args=())
	IRThread.setDaemon(True)
	IRThread.start()

	AccThread = threading.Thread(target=runAcc, args=())
	AccThread.setDaemon(True)
	AccThread.start()

def runAcc():
	while 1:
		try:
			if(AccIn == None):
				AccIn = open('/dev/input/event3','r')
			array = readFrom(AccIn)
			accessory['connected'] = 'Nunchuck'

			if(array[4] == '0001'):
				if(array[6] == '0001'):
					state = True
				else:
					state = False
				if(array[5] == '0132'):
					accessory['buttons']['C'] = state
				elif(array[5] == '0135'):
					accessory['buttons']['Z'] = state

			elif(array[4] == '0003'):
				if(array[5] == '0010'):
					if(array[7] == 'FFFF'):
						accessory['stick']['x'] = int(array[6], 16) - 65536
					else:
						accessory['stick']['x'] = int(array[6], 16)
				elif(array[5] == '0011'):
					if(array[7] == 'FFFF'):
						accessory['stick']['y'] = int(array[6], 16) - 65536
					else:
						accessory['stick']['y'] = int(array[6], 16)

				elif(array[5] != '0003' and array[5] != '0004' and array[5] != '0005'):
					print array

			elif(array[4] != '0000'):
				print array
		except:
			accessory['connected'] = None
			AccIn = None
			
def runIR():
	IRIn = open('/dev/input/event1','r')
	while 1:
		array = readFrom(IRIn)
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

def runButton():
	ButtonsIn = open('/dev/input/event2','r')
	while 1:
		array = readFrom(ButtonsIn)
		if(array[4] == '0001'): #Button Press
			state = False
			if(array[6] == '0001'):
				state = True
			elif(array[6] == '0000'):
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
			#A B 1 2
			elif(array[5]=='0130'):
				buttons['A'] = state
			elif(array[5]=='0131'):
				buttons['B'] = state
			elif(array[5]=='0101'):
				buttons['1'] = state
			elif(array[5]=='0102'):
				buttons['2'] = state
			#- Home +
			elif(array[5]=='019C'):
				buttons['-'] = state
			elif(array[5]=='0197'):
				buttons['+'] = state
			elif(array[5]=='013C'):
				buttons['Home'] = state
