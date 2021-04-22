"""
handles input / output
"""
import globals as gl
import pygame

pygame_events = None

""" ### ### general input via keyboard ### ### """
def keyboard_input():
	global pygame_events

	pygame_events = pygame.event.get()			# save all current events

	for event in pygame_events:					# check for keyboard input
			# closing window / exit program
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				gl.prog_active = False
			if event.type == pygame.KEYDOWN:
				# debug information
				if event.key == pygame.K_d:
					gl.show_debug = not gl.show_debug
				# return to intro
				if event.key == pygame.K_i:
					gl.prog_pos = 'i'

""" ### ### INPUT ### ### """
UP, DOWN, LEFT, RIGHT, NEXT, BACK = 26, 19, 3, 4, 2, 21		# NOTE Buttons: set corresponding pins here
up_state, down_state, left_state, right_state, next_state, back_state = False, False, False, False, False, False			# saves pin state
up_state_prev, down_state_prev, left_state_prev, right_state_prev, next_state_prev, back_state_prev = False, False, False, False, False, False			# saves previous pin state

if gl.os_is_linux:								# create button objects to read gpio pins
	from gpiozero import Button
	UP_BT, DOWN_BT, LEFT_BT, RIGHT_BT, NEXT_BT, BACK_BT = Button(UP), Button(DOWN), Button(LEFT), Button(RIGHT), Button(NEXT), Button(BACK)

def update_input():
	""" update all  / reads the input and stores it to be returned by read_input() """
	global UP, DOWN, LEFT, RIGHT, NEXT, BACK, pygame_events
	global up_state, down_state, left_state, right_state, next_state, back_state
	global up_state_prev, down_state_prev, left_state_prev, right_state_prev, next_state_prev, back_state_prev


	if gl.os_is_linux:
		global UP_BT, DOWN_BT, LEFT_BT, RIGHT_BT, NEXT_BT, BACK_BT		

	# refresh previous states
	up_state_prev, down_state_prev, left_state_prev, right_state_prev, next_state_prev, back_state_prev = up_state, down_state, left_state, right_state, next_state, back_state

	# read current state
	if gl.os_is_linux:				# for the raspberry pi / buttons on gpio
		up_state	= not UP_BT.is_pressed			# read every input
		down_state	= not DOWN_BT.is_pressed
		left_state	= not LEFT_BT.is_pressed
		right_state	= not RIGHT_BT.is_pressed
		next_state	= not NEXT_BT.is_pressed
		back_state	= not BACK_BT.is_pressed

	# for keyboard
	for event in pygame_events:
		if event.type == pygame.KEYDOWN:		# if pressed down
			if(event.key == pygame.K_UP):		up_state 	= True
			if(event.key == pygame.K_DOWN):		down_state 	= True
			if(event.key == pygame.K_LEFT):		left_state 	= True
			if(event.key == pygame.K_RIGHT):	right_state = True
			if(event.key == pygame.K_RETURN):	next_state 	= True
			if(event.key == pygame.K_DELETE):	back_state 	= True
		if event.type == pygame.KEYUP:			# if released
			if(event.key == pygame.K_UP):		up_state 	= False
			if(event.key == pygame.K_DOWN):		down_state 	= False
			if(event.key == pygame.K_LEFT):		left_state 	= False
			if(event.key == pygame.K_RIGHT):	right_state = False
			if(event.key == pygame.K_RETURN):	next_state 	= False
			if(event.key == pygame.K_DELETE):	back_state 	= False

	
		# check for credits
		if up_state or (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB):
			if down_state and left_state and right_state and next_state and back_state or (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB):
				print("[IO UI] go to credits")
				gl.cr_prev_pos = gl.prog_pos
				gl.prog_pos = 'cr'

def read_input(input):
	""" returns input state as bool
	input: key [UP, DOWN, LEFT, RIGHT, NEXT, BACK]
	"""
	global UP, DOWN, LEFT, RIGHT, NEXT, BACK
	global up_state, down_state, left_state, right_state, next_state, back_state
	global up_state_prev, down_state_prev, left_state_prev, right_state_prev, next_state_prev, back_state_prev


	keys = [(UP, up_state, up_state_prev), (DOWN, down_state, down_state_prev),
			(LEFT, left_state, left_state_prev), (RIGHT, right_state, right_state_prev),
			(NEXT, next_state, next_state_prev), (BACK, back_state, back_state_prev)]			# list of possible inputs and matching states

	is_pressed = False				# this variable will be set True when asked button is pressed. Otherwise it won't change

	for key in keys:				# loops through key list
		if key[0] == input and key[2] == False:		# if tested key equals input and requested key is pressed
			is_pressed = key[1]						# set is_pressed = True
	
	return is_pressed

""" ### ### OUTPUT ### ### """

VALVES = [8, 7, 1, 24, 15, 18]			# NOTE Valves: set corresponding pins here ([0] is the valve for water, then going from left to right)
PUMP = 23								#		Pump:  set pin for pump here
if gl.os_is_linux:
	from gpiozero import LED
	VALVES_OUT = [LED(VALVES[0]), LED(VALVES[1]), LED(VALVES[2]), LED(VALVES[3]), LED(VALVES[4]), LED(VALVES[5])]		# create led objects to controll valves and pump
	PUMP_OUT = LED(PUMP)
	
	for i in VALVES_OUT:		# setting the output state to high, to switch relais-board off
		i.on()
	PUMP_OUT.on()
	
valves_state = [False, False, False, False, False, False]			# states of the pins
pump_state = False

def write_output(out, state):
	""" set output
	out: pin to set [VALVES[0:7], PUMP] or any other gpio pin
	state: state [True / 1, False / 0]
	"""
	global HIGH, LOW, VALVES, PUMP, valves_state, pump_state
	global VALVES_OUT, PUMP_OUT

	if gl.os_is_linux:			# for the raspberry pi
		# list of possible outputs and matching led objects
		keys = [(VALVES[0], VALVES_OUT[0]), (VALVES[1], VALVES_OUT[1]), (VALVES[2], VALVES_OUT[2]),
				(VALVES[3], VALVES_OUT[3]), (VALVES[4], VALVES_OUT[4]), (VALVES[5], VALVES_OUT[5]),
				(PUMP, PUMP_OUT)]		
		for key in keys:
			if key[0] == out:
				if state == True:
					key[1].off()
				else:
					key[1].on()
	
	# keep the saved states up-to-date
	for idx, valve in enumerate(VALVES):
		if out == valve:
			valves_state[idx] = state
	if out == PUMP:
		pump_state = state
