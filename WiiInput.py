import sys
from collections import OrderedDict

pipe = open('/dev/input/event2','r')
data = ''
array = []
buttons = OrderedDict([('A', False), ('B', False), ('1', False), ('2', False), ('Up', False), ('Down', False), ('Left', False), ('Right', False),  ('-', False), ('+', False), ('Home', False)])
ir = { 'x':0, 'y':0 } #TODO: IR Support
#TODO: Gyro Support
def runInputButton():
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
		testRaw = array[5]
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
