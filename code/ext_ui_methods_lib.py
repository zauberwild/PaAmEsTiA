"""
this file include all methods for the user interface
"""

import globals as gl
import media_lib
import drinks_lib as drinks
import io_lib as io

""" ### ### SETUP / LOOP ### ### """
""" actions that need to be executed once on startup are here 
	This includes object creation, reading files in, etc.
"""

# intro
introduction_vid = media_lib.Video("/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")

""" EOF SETUP """

def loop():
	""" actions that need to be executed every loop (independently from prog_pos are here)
		this method will be called before any other actions in the main loop
	"""
	io.keyboard_input()		# keyboard input
	io.update_input()		# button input

	drinks.update_mixing()		# update mixing process

	# debug information about input and output
	if gl.show_debug:
		if not gl.prog_pos == 'i':
			i_s = "O: "
			for i in io.valves_state:
				i_s += str(int(i)) + "; "
			i_s += str(int(io.pump_state))
			gl.debug_text.append(i_s)
			i_s = "I: up: " + str(int(io.readInput(io.UP))) + "; down: " + str(int(io.readInput(io.DOWN))) + "; left: " + str(int(io.readInput(io.LEFT))) + "; right: " + str(int(io.readInput(io.RIGHT))) + ";"
			gl.debug_text.append(i_s)
			i_s = "I: next: " + str(int(io.readInput(io.NEXT))) + "; back: " + str(int(io.readInput(io.BACK)))
			gl.debug_text.append(i_s)

""" ### ### INTRO / MAIN MENU ### ### """
intro_active = False
def intro():
	gl.prog_pos = 'm'		# DEL as soon as intro needed again

	global intro_active, introduction_vid

	if intro_active == False:
		intro_active = True
		introduction_vid.start(audio=False)			# start intro
	
	introduction_vid.draw()				# draw intro

	if introduction_vid.test_for_last_frame():			# test if intro is ending
		intro_active = False
		gl.prog_pos = 'm'

menu_active = False
menu_btns = []
menu_pos = 0

def main_menu():
	global menu_active, btn1, btn2, btn3, menu_pos, test_recipe	
	
	if menu_active == False:			# setup
		menu_active = True
		menu_btns.append(media_lib.Button("/src/props/", "prop_white.png", "prop_green.png"	, "prop_grey.png", 150, 69, 500, 64))
		menu_btns.append(media_lib.Button("/src/props/", "prop_white.png", "prop_blue.png"	, "prop_grey.png", 150, 202, 500, 64))
		menu_btns.append(media_lib.Button("/src/props/", "prop_white.png", "prop_yellow.png", "prop_grey.png", 150, 335, 500, 64))
		menu_btns.append(media_lib.Button("/src/props/", "prop_white.png", "prop_red.png"	, "prop_grey.png", 150, 468, 500, 64))
		menu_btns[0].add_text("REZEPT AUSWAEHLEN", gl.debug_font_big, (0,0,0), 0)
		menu_btns[1].add_text("FREI MISCHEN", gl.debug_font_big, (0,0,0), 0)
		menu_btns[2].add_text("EINSTELLUNGS", gl.debug_font_big, (0,0,0), 0)
		menu_btns[3].add_text("VERLASSEN", gl.debug_font_big, (0,0,0), 0)
	
	# input
	# go up or down
	if io.readInput(io.UP):
		menu_pos -= 1
	if io.readInput(io.DOWN):
		menu_pos += 1

	# select menu item
	if io.readInput(io.NEXT):
		if menu_pos == 0:
			gl.prog_pos = 'rt'
		elif menu_pos == 1:
			gl.prog_pos = 'ft'
		elif menu_pos == 2:
			gl.prog_pos = 's'
		elif menu_pos == 3:
			gl.prog_pos = 'q'
	
	# logic
	# menu boundaries
	if menu_pos < 0:
		menu_pos = 0
	if menu_pos > 3:
		menu_pos = 3
	
	# selected item
	for idx, btn in enumerate(menu_btns):
		if idx == menu_pos:
			btn.selected = True
		else:
			btn.selected = False

	# draw
	gl.screen.fill((127,127,127))
	for btn in menu_btns:
		btn.draw()

	gl.debug_text.append("menu_pos: " + str(menu_pos))

""" ### ### FREE MIXING ### ### """
def free_transition():
	gl.prog_pos = 'fc'

def free_choose():
	pass

def free_output():
	pass


""" ### ### RECIPE ### ### """
rt_active = False
def recipe_transition():
	global rt_active

	if rt_active == False:
		rt_active = True

	gl.prog_pos = 'rc'

rc_active = False
rc_btns = []
rc_pos = 0
rc_stage = 0		#0: show all recipes; 1: show info of selected recipe (-1: go back; 2: mix recipe)
def recipe_choose():
	global rc_active, rc_btns, rc_pos, rc_stage

	# entering the menu
	if rc_active == False:
		rc_active = True
		rc_stage = 0
		height = 64
		btn_size = (420, 40)
		rc_btns.clear()
		for i in drinks.recipes:
			rc_btns.append(media_lib.Button("/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 20, height, btn_size[0], btn_size[1]))
			rc_btns[-1].add_text(i, gl.debug_font, (0,0,0), 1)
			height += btn_size[1] + 15

	# input
	if rc_stage == 0:
		if io.readInput(io.UP):
			rc_pos -= 1
		if io.readInput(io.DOWN):
			rc_pos += 1

	# select menu item
	if io.readInput(io.NEXT):
		rc_stage += 1
	# go back
	if io.readInput(io.BACK):
		rc_stage -= 1

	# logic
	# menu boundaries
	if rc_pos < 0:
		rc_pos = 0
	elif rc_pos > len(rc_btns)-1:
		rc_pos = len(rc_btns)-1

	# selected item
	for idx, btn in enumerate(rc_btns):
		if idx == rc_pos:
			btn.selected = True
		else:
			btn.selected = False
	
	# going back
	if rc_stage == -1:
		gl.prog_pos = 'm'
		rc_active = False

	# draw
	gl.screen.fill((127,127,127))
	if rc_stage == 0:
		for i in rc_btns:
			i.draw()

def recipe_output():
	pass


""" ### ### SETTINGS ### ### """
def settings():
	pass

""" ### SHUTDOWN ### """
def shutdown():
	print("STOPPING PROGRAM")
	gl.prog_active = False
