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
	# DEL if not needed
"""

file = open(gl.gen_path + "/src/drinks")
lines = file.readlines()
for idx, val in enumerate(range(0,6)):
	drinks.set_drink(idx, val)
""" EOF SETUP """

def loop():
	""" actions that need to be executed every loop (independently from prog_pos) are here.
		this function will be called before any other actions in the main loop
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

introduction_vid = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")

def intro():
	gl.prog_pos = 'rc'		# DEL as soon as intro is needed again

	global intro_active, introduction_vid

	if intro_active == False:		# setup
		intro_active = True
		introduction_vid.start(audio=False)			# start intro
	
	introduction_vid.draw()				# draw intro

	if introduction_vid.test_for_last_frame():			# test if intro is ending
		intro_active = False
		introduction_vid = None
		gl.prog_pos = 'm'


menu_active = False
menu_btns = []
menu_pos = 0

def main_menu():
	global menu_active, menu_btns, menu_pos, test_recipe	
	
	if menu_active == False:			# setup
		menu_active = True
		# creating the buttons for the main menu
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png"	, "prop_grey.png", 150, 69, 500, 64))
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_blue.png"	, "prop_grey.png", 150, 202, 500, 64))
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_yellow.png", "prop_grey.png", 150, 335, 500, 64))
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_red.png"	, "prop_grey.png", 150, 468, 500, 64))
		menu_btns[0].add_text("REZEPT AUSWAEHLEN", gl.debug_font_big, (0,0,0), 0)
		menu_btns[1].add_text("FREI MISCHEN", gl.debug_font_big, (0,0,0), 0)
		menu_btns[2].add_text("EINSTELLUNGEN", gl.debug_font_big, (0,0,0), 0)
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
			gl.prog_pos = 'st'
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

	# for each button in list
	for btn in menu_btns:
		btn.draw()

	# append debug information
	if gl.show_debug:
		gl.debug_text.append("menu_pos: " + str(menu_pos))




""" ### ### FREE MIXING ### ### """
ft_active = False
ft_video = None
def free_transition():
	global ft_active, ft_video

	if ft_active == False:
		ft_active = True
		ft_video = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")
		ft_video.start()

	ft_video.draw()

	if ft_video.test_for_last_frame():
		ft_video = None
		gl.prog_pos = 'fc'

fc_active = False
fc_background = None
fc_buttons = []
fc_bars = []
fc_sum_text = None

fc_pos = 1			# position on the menu (0: go back, 1-5: drinks, 6: next)
fc_values = []		# saves values for the drinks

def free_choose():
	global fc_active, fc_background, fc_buttons, fc_bars, fc_pos, fc_values, fc_sum_text
	
	# entering free_choose
	if fc_active == False:
		fc_active = True
		# set video background
		fc_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")
		fc_background.start(repeat=True, audio=False)

		# set buttons
			# go back
		fc_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_grey.png", "prop_tri_green.png", "prop_white.png", 20, 500, 60, 60, rotation=270))
		

			# button with the drinks and bars
		spacing = 50
		btn_width, btn_height = 100, 60
		btn_x, btn_y = spacing, 400
		for i in drinks.plugs[1:]:
			fc_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_white.png", btn_x, btn_y, btn_width, btn_height))
			fc_buttons[-1].add_text(i, gl.debug_font_small, (255,0,0))

			fc_bars.append("#TODO add the bars")
			fc_values.append(0)
			btn_x += btn_width + spacing

		fc_buttons[fc_pos].selected = True

			# next
		fc_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_grey.png", "prop_tri_green.png", "prop_white.png", 800-60-20, 500, 60, 60, rotation=90))

		# textfield for sum
		fc_sum_text = media_lib.TextField(400-50, 20, 100, 45, "ph", gl.debug_font, (255,0,0), alignment=0)
		fc_sum_text.add_background(gl.gen_path + "/src/props/prop_white.png")

	""" logic / input """
	# go left or right
	if io.readInput(io.LEFT):
		fc_buttons[fc_pos].selected = False
		fc_pos -= 1
		if fc_pos < 0:
			fc_pos = 0
		fc_buttons[fc_pos].selected = True
	if io.readInput(io.RIGHT):
		fc_buttons[fc_pos].selected = False
		fc_pos += 1
		if fc_pos > len(fc_buttons)-1:
			fc_pos = len(fc_buttons)-1
		fc_buttons[fc_pos].selected = True

	# raising  / lowering values
	interval = 10
	sum_values = sum(fc_values)
	if io.readInput(io.UP) and sum_values < 100:			# when raising a value, but sum is less than 100%
		if fc_pos > 0 and fc_pos < len(fc_buttons)-1:
			fc_values[fc_pos-1] += interval
			if fc_values[fc_pos-1] > 100:
				fc_values[fc_pos-1] = 100
	if io.readInput(io.DOWN):
		if fc_pos > 0 and fc_pos < len(fc_buttons)-1:
			fc_values[fc_pos-1] -= interval
			if fc_values[fc_pos-1] < 0:
				fc_values[fc_pos-1] = 0

	fc_sum_text.change_text(str(sum_values) + "%")
				val = int((gl.GLASS_SIZE / 100) * val)							# converts the relative value (#HACK: from 0 to 100, not 0 to 1)
																				# to an absolute value from 0 to gl.GLASS_SIZE using a linear function

	""" draw """
	fc_background.draw()

	fc_sum_text.draw()

	for btn in fc_buttons:
		btn.draw()

	

def free_output():
	pass




""" ### ### RECIPE ### ### """
rt_active = False
rt_video = None
def recipe_transition():
	gl.prog_pos ='rc'			# DEL when finished
	global rt_active, rt_video

	if rt_active == False:
		rt_active = True
		rt_video = media_lib.Video(gl. gen_path + "/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")
		rt_video.start(audio=False)

	rt_video.draw()

	if rt_video.test_for_last_frame():
		rt_video = None
		gl.prog_pos = 'rc'

rc_active = False
rc_visible_n = 6			# number of visible items
rc_btns = []				# list holding the recipes buttons
rc_pos = 0					# position of selection in complete recipe list
rc_visible_pos = 0			# position in visible part

rc_recipes = []				# list of all recipes, sorted after availability, than alphabetically

rc_marker = []				# list holding markers

rc_background = None		# video in the background

rc_stage = 0				#0: show all recipes; 1: show info of selected recipe (-1: go back; 2: mix recipe)
rc_info_textfield = None	# holds a textfield as soon stage is set to showing info

def recipe_choose():
	global rc_active, rc_btns, rc_pos, rc_visible_pos, rc_recipes, rc_stage, rc_marker, rc_background, rc_info_textfield

	# entering the menu
	if rc_active == False:
		rc_active = True

		# filling recipe list
		list1 = drinks.get_recipes(available=True)
		list1.sort()
		list2 = drinks.get_recipes(available=False)
		list2.sort()
		rc_recipes = list1 + list2

		# creating background
		rc_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")
		rc_background.start(repeat=True, audio=False)

		# creating buttons
		btn_size = (420, 40)
		spacing = 20
		height = (600 - (btn_size[1]*rc_visible_n) - (spacing*rc_visible_n-1))/2
		rc_btns.clear()
		for i in range(rc_visible_n):
			rc_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 20, height, btn_size[0], btn_size[1]))
			height += btn_size[1] + spacing

		# creating marker
		rc_marker.clear()
		rc_marker.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_green.png", "prop_white.png", "prop_tri_grey.png", 100, 50, 220, 50, rotation=180))
		rc_marker.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_green.png", "prop_white.png", "prop_tri_grey.png", 100, 500, 220, 50))


	""" input """
	# go up or down
	if rc_stage == 0:					# ony if in list mode
		if io.readInput(io.UP):
			rc_visible_pos -= 1
			rc_pos -= 1
		if io.readInput(io.DOWN):
			rc_visible_pos += 1
			rc_pos += 1

	# select menu item / start mixing
	if io.readInput(io.NEXT) or io.readInput(io.RIGHT):
		rc_stage += 1
	# go back to menu / list
	if io.readInput(io.BACK) or io.readInput(io.LEFT):
		rc_stage -= 1

	""" logic """
	# menu boundaries
	# visible part
	if rc_visible_pos < 0:
		rc_visible_pos = 0
	elif rc_visible_pos > rc_visible_n-1:
		rc_visible_pos = rc_visible_n-1
	# complete list
	if rc_pos < 0:
		rc_pos = 0
	elif rc_pos > len(rc_recipes)-1:
		rc_pos = len(rc_recipes)-1
	
	# moving menu / setting correct text
	a = rc_pos - rc_visible_pos 		# first visible item
	for btn in rc_btns:
		btn.add_text(rc_recipes[a], gl.debug_font, (0,0,0), 1)
		a += 1

	# control marker
	# upper marker
	if rc_btns[0].text == rc_recipes[0]:	# if first item in recipe-list is visible -> we are on the top of the list
		rc_marker[0].disabled = True
	else:
		rc_marker[0].disabled = False
	# lower marker
	if rc_btns[-1].text == rc_recipes[-1]:	# if last item in recipe-list is visible -> we are on the bottom of the list
		rc_marker[1].disabled = True
	else:
		rc_marker[1].disabled = False

	# selected item
	for idx, btn in enumerate(rc_btns):
		if idx == rc_visible_pos:
			btn.selected = True
		else:
			btn.selected = False

	# showing info
	if rc_stage == 1 and not rc_info_textfield:
		chosen_recipe = None			# find the chosen recipe
		for btn in rc_btns:
			if btn.selected:
				chosen_recipe = btn.text
		file = open(gl .gen_path + "/src/recipes/" + chosen_recipe, 'r')
		text = file.readline()		# read the first line (info about recipe)
		file.close()
		
		# create textfield
		rc_info_textfield = media_lib.TextField(50, 50, 400, 400, text, gl.debug_font_small, (0,0,255), alignment=1)
		rc_info_textfield.add_background(gl.gen_path + "/src/props/prop_yellow.png")
		
	# disabling info
	if rc_stage == 0 and rc_info_textfield:
		rc_info_textfield = None
			
	# navigating back and forwards
	if rc_stage == -1:					# going back
		gl.prog_pos = 'm'
		rc_active = False
	elif rc_stage == 2:					# start mixing
		chosen_recipe = None			# find the chosen recipe
		for btn in rc_btns:
			if btn.selected:
				chosen_recipe = btn.text
		
		drinks.start_mixing(chosen_recipe)		# start mixing procedure
		if drinks.is_mixing:					# if really started
			gl.prog_pos = 'ro'					# go to recipe output
		else:
			rc_stage = 1

	# draw
	rc_background.draw()
	if rc_stage == 0:					# list mode
		for i in rc_btns:
			i.draw()
		for i in rc_marker:
			i.draw()
	elif rc_stage == 1:					# info mode
		rc_info_textfield.draw()


	# if leaving recipe choose, clean up variables
	if gl.prog_pos != 'rc':
		rc_active = False
		rc_btns.clear()
		rc_stage = 0
		rc_marker.clear()
		rc_background = None
		rc_info_textfield = None
		rc_recipes.clear()

	# debug information
	if gl.show_debug:
		gl.debug_text.append("rc_pos: " + str(rc_pos) + 
							"; rc_visible_pos: " + str(rc_visible_pos) + 
							"; rc_stage: " + str(rc_stage))

ro_active = False
ro_background = None
def recipe_output():
	global ro_active, ro_background

	if not ro_active:		# if first entering recipe output
		ro_active = True
		ro_background = media_lib.Video("/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")
		ro_background.start(audio=False, repeat=True)
		print("[UI RO] now mixing")

	ro_background.draw()


	if not drinks.is_mixing:		# if leaving recipe_output
		print("[UI RO] mixing done")
		ro_active = False
		ro_background = None
		gl.prog_pos = 'rc'




""" ### ### SETTINGS ### ### """
st_active = False
st_video = None
def settings_transition():
	global st_active, st_video

	if st_active == False:
		st_active = True
		st_video = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4", "/src/media/intro/audio.wav")
		st_video.start()

	st_video.draw()

	if st_video.test_for_last_frame():
		st_video = None
		gl.prog_pos = 'sc'


def settings():
	pass



""" ### SHUTDOWN ### """
def shutdown():
	print("STOPPING PROGRAM")
	if gl.os_is_linux:
		from subprocess import call
		call("sudo shutdown -h now", shell=True)
	gl.prog_active = False
