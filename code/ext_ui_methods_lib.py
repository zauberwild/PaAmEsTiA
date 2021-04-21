"""
this file include all methods for the user interface
"""

from tkinter.constants import TRUE
from numpy import true_divide
import globals as gl
import io_lib as io
import media_lib
import drinks_lib as drinks

""" ### ### SETUP / LOOP ### ### """
""" actions that need to be executed once on startup are here 
	This includes object creation, reading files in, etc.
	# DEL if not needed
"""

file = open(gl.gen_path + "/src/drinks")
lines = file.readlines()
for idx, i in enumerate(lines):						# remove trailing newline characters
	if lines[idx].endswith('\n'):
		lines[idx] = lines[idx][:-1]
print("[UI setup] drink file content:")
print(lines)
for idx, val in enumerate(lines):
	drinks.set_drink(idx, val)


""" EOF SETUP """

def loop():
	""" actions that need to be executed every loop (independently from prog_pos) are here.
		this function will be called before any other actions in the main loop
	"""
	io.keyboard_input()		# keyboard input
	io.update_input()		# button input

	# debug information about input and output
	if gl.show_debug:
		if not gl.prog_pos == 'i':
			i_s = "O: "
			for i in io.valves_state:
				i_s += str(int(i)) + "; "
			i_s += str(int(io.pump_state))
			gl.debug_text.append(i_s)
			i_s = "I: up: " + str(int(io.read_input(io.UP))) + "; down: " + str(int(io.read_input(io.DOWN))) + "; left: " + str(int(io.read_input(io.LEFT))) + "; right: " + str(int(io.read_input(io.RIGHT))) + ";"
			gl.debug_text.append(i_s)
			i_s = "I: next: " + str(int(io.read_input(io.NEXT))) + "; back: " + str(int(io.read_input(io.BACK)))
			gl.debug_text.append(i_s)




""" ### ### INTRO / MAIN MENU ### ### """
intro_active = False

introduction_vid = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")

def intro():
	global intro_active, introduction_vid

	gl.prog_pos = 'rc'		# DEL as soon as intro is needed again
	intro_active = False

	if intro_active == False:		# setup
		intro_active = True
		introduction_vid.start()			# start intro
	
	introduction_vid.draw()				# draw intro

	if introduction_vid.test_for_last_frame() or intro_active == False:			# test if intro is ending
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
	if io.read_input(io.UP):
		menu_pos -= 1
	if io.read_input(io.DOWN):
		menu_pos += 1

	# select menu item
	if io.read_input(io.NEXT):
		if menu_pos == 0:
			gl.prog_pos = 'rc'
		elif menu_pos == 1:
			gl.prog_pos = 'fc'
		elif menu_pos == 2:
			gl.prog_pos = 'sc'
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

fc_active = False			# controls if free_choose is active or not
fc_background = None		# saves the background video
fc_buttons = []				# saves the buttons at the buttom
fc_bars = []				# saves the (progress) bars
fc_sum_text = None			# saves the textfield showing the sum of all drinks

fc_pos = 1					# position on the menu (0: go back, 1-5: drinks, 6: next)
fc_values = [0,0,0,0,0]		# saves values for the drinks

def free_choose():
	global fc_active, fc_background, fc_buttons, fc_bars, fc_pos, fc_values, fc_sum_text
	
	# entering free_choose
	if fc_active == False:
		fc_active = True
		# set video background
		fc_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")
		fc_background.start(repeat=True)

		# set buttons
			# button: go back
		fc_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_grey.png", "prop_tri_green.png", "prop_white.png", 20, 500, 60, 60, rotation=270))
		

			# buttons with the drinks and bars
		spacing = 50
		btn_width, btn_height = 100, 60
		btn_x, btn_y = spacing, 400
		bar_y, bar_height = 100, 250
		print("[UI FC]", drinks.plugs)
		for e, i in enumerate(drinks.plugs[1:]):
			# buttons
			fc_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_white.png", btn_x, btn_y, btn_width, btn_height))
			fc_buttons[-1].add_text(i, gl.debug_font_small, (255,0,0))

			# bars
			fc_bars.append(media_lib.Bar(gl.gen_path + "/src/props/bar/", btn_x, bar_y, btn_width, bar_height, state=fc_values[e]))
			
			# increase counter
			btn_x += btn_width + spacing

			# button: next
		fc_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_grey.png", "prop_tri_green.png", "prop_white.png", 800-60-20, 500, 60, 60, rotation=90))

		fc_buttons[fc_pos].selected = True

		# textfield for sum
		fc_sum_text = media_lib.TextField(400-50, 20, 100, 45, "ph", gl.debug_font, (255,0,0), alignment=0)
		fc_sum_text.add_background(gl.gen_path + "/src/props/prop_white.png")

	""" logic / input """
	# go left or right
	if io.read_input(io.LEFT):
		fc_buttons[fc_pos].selected = False
		fc_pos -= 1
		if fc_pos < 0:
			fc_pos = 0
		fc_buttons[fc_pos].selected = True
	if io.read_input(io.RIGHT):
		fc_buttons[fc_pos].selected = False
		fc_pos += 1
		if fc_pos > len(fc_buttons)-1:
			fc_pos = len(fc_buttons)-1
		fc_buttons[fc_pos].selected = True

	# raising  / lowering values
	interval = 10
	sum_values = sum(fc_values)

	if fc_pos > 0 and fc_pos < len(fc_buttons)-1:			# checking if a drink (and not go back / next) is selected
		if io.read_input(io.UP) and sum_values < 100:			# when raising a value, but sum is less than 100%
			fc_values[fc_pos-1] += interval
			if fc_values[fc_pos-1] > 100:					# upper boundary
				fc_values[fc_pos-1] = 100
		if io.read_input(io.DOWN):
			fc_values[fc_pos-1] -= interval
			if fc_values[fc_pos-1] < 0:						# lower boundary
				fc_values[fc_pos-1] = 0

		fc_bars[fc_pos-1].set_state(fc_values[fc_pos-1])	# set the new state for selected bar

	fc_sum_text.change_text(str(sum_values) + "%")			# change the text for the summ of all drinks


	# exiting the menu or start mixing
	if io.read_input(io.BACK) or (io.read_input(io.NEXT) and fc_pos == 0):		# if back pressed or back selected
		fc_active = False
		gl.prog_pos = 'm'
	if io.read_input(io.NEXT) and not fc_pos == 0:								# if next pressed and not back selected
		file = open(drinks.dir_recipes + "free_mixed_recipe", 'w')				# open file
		file.truncate(0)														# delete content
		file.write("this file contains a self mixed recipe\n")					# write first line
		for idx, val in enumerate(fc_values):									# for every drink with value more than zero,
			if val > 0:
				val = int((gl.GLASS_SIZE / 100) * val)							# converts the relative value (#HACK: from 0 to 100, not 0 to 1)
																				# to an absolute value from 0 to gl.GLASS_SIZE using a linear function
				text = str(drinks.plugs[idx+1]) + "," + str(val)				# prepare text (idx+1, because the first one would be cleanig_water)
				file.write(text+"\n")											# add to file with name and amount
		file.close()															# close file

		drinks.start_mixing("free_mixed_recipe")								# start the micing procedure with the freshly written file

		fc_active = False				# also, leave this menu
		gl.prog_pos = 'fo'				# and go to free_output

	""" draw """
	fc_background.draw()

	fc_sum_text.draw()

	for bar in fc_bars:
		bar.draw()

	for btn in fc_buttons:
		btn.draw()

	""" if leaving this menu, clear all big variables/objects up """
	if fc_active == False:
		fc_background = None
		fc_buttons.clear()
		fc_bars.clear()
		fc_sum_text = None

	""" add debug info """
	if gl.show_debug:
		t = "fc_values: "
		for i in fc_values:
			t += str(i) + ", "
		gl.debug_text.append(t)

	
fo_active = False
fo_background = None
def free_output():
	global fo_active, fo_background

	if not fo_active:		# if first entering recipe output
		fo_active = True
		fo_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")
		fo_background.start(repeat=True)
		print("[UI FO] now mixing")

	fo_background.draw()
	drinks.update_mixing()		# update mixing process

	if not drinks.get_still_mixing():
		print("[UI FO] free mixing done")

		fo_active = False
		fo_background = None
		gl.prog_pos = 'fc'




""" ### ### RECIPE ### ### """

rc_active = False
rc_visible_n = 6			# number of visible items
rc_btns = []				# list holding the recipes buttons
rc_pos = 0					# position of selection in complete recipe list
rc_visible_pos = 0			# position in visible part

rc_recipes = []				# list of all recipes, sorted after availability, than alphabetically

rc_marker = []				# list holding markers

rc_std_file = "/src/media/intro/intro.mp4"	# standard video file
rc_background = None		# video in the background

rc_stage = 0				# 0: show all recipes; 1: show info of selected recipe (-1: go back; 2: mix recipe)
rc_info_textfield = None	# holds a textfield as soon stage is set to showing info
rc_info_btns = []			# holds all objects for info screen

def recipe_choose():
	global rc_active, rc_btns, rc_pos, rc_visible_pos, rc_recipes, rc_stage, rc_marker, rc_std_file, rc_background, rc_info_textfield, rc_info_btns

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
		rc_background = media_lib.Video(gl.gen_path + rc_std_file)
		rc_background.start(repeat=True)

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
		if io.read_input(io.UP):
			rc_visible_pos -= 1
			rc_pos -= 1
		if io.read_input(io.DOWN):
			rc_visible_pos += 1
			rc_pos += 1

	# select menu item / start mixing
	if io.read_input(io.NEXT) or io.read_input(io.RIGHT):
		rc_stage += 1
	# go back to menu / list
	if io.read_input(io.BACK) or io.read_input(io.LEFT):
		rc_stage -= 1

	""" logic """
	chosen_recipe = None			# find the chosen recipe
	for btn in rc_btns:
		if btn.selected:
			chosen_recipe = btn.text

	if (io.read_input(io.UP) or io.read_input(io.DOWN)) and rc_stage == 0:
		# setting correct background
		prev_file = rc_background.file
		try:
			new_file = gl.gen_path + gl.recipe_video_dict[chosen_recipe]
		except KeyError:
			new_file = gl.gen_path + rc_std_file
		if prev_file != new_file:
			rc_background.file = new_file
			rc_background.start(repeat=True, frame_counter=rc_background.frame_counter)
	
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
		file = open(gl .gen_path + "/src/recipes/" + chosen_recipe, 'r')
		text = file.readline()		# read the first line (info about recipe)
		file.close()
		
		# create textfield
		rc_info_textfield = media_lib.TextField(50, 50, 400, 400, text, gl.debug_font_small, (0,0,255), alignment=1)
		rc_info_textfield.add_background(gl.gen_path + "/src/props/prop_yellow.png")
		#creating info objects
		rc_info_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_grey.png", "prop_white.png", "prop_white.png", 50, 500, 75, 75, rotation=270))
		rc_info_btns[-1].add_text("BACK", gl.standard_font, (0,0,255))
		rc_info_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_grey.png", "prop_white.png", "prop_white.png", 700, 500, 75, 75, rotation=90))
		rc_info_btns[-1].add_text("MISCHEN", gl.standard_font, (0,0,255))
		rc_info_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_grey.png", "prop_white.png", "prop_white.png", 300, 500, 475, 75))
		rc_info_btns[-1].add_text("MISCHEN NICHT MÖGLICH", gl.standard_font, (0,0,255))
		
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
		rc_info_btns[0].draw()
		if drinks._test_availability(chosen_recipe):
			rc_info_btns[1].draw()
		else:
			rc_info_btns[2].draw()

	# if leaving recipe choose, clean up variables
	if gl.prog_pos != 'rc':
		rc_active = False
		rc_btns.clear()
		rc_stage = 0
		rc_marker.clear()
		rc_background = None
		rc_info_textfield = None
		rc_info_btns.clear()
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
		ro_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")
		ro_background.start(repeat=True)
		print("[UI RO] now mixing")

	ro_background.draw()
	drinks.update_mixing()		# update mixing process


	if not drinks.is_mixing:		# if leaving recipe_output
		print("[UI RO] mixing done")
		ro_active = False
		ro_background = None
		gl.prog_pos = 'rc'




""" ### ### SETTINGS ### ### """
# settings: selection menu
sc_active = False
sc_background = None			# background
sc_btns = []					# list of all buttons
sc_pos = 0						# positon / selected button

def settings_choose():
	global sc_active, sc_background, sc_btns, sc_pos

	if sc_active == False:		# when entering settings_choose
		sc_active = True
		sc_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")		# create background
		sc_background.start(repeat=True)

		# create buttons
		sc_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 35, 35, 300, 530))
		sc_btns[-1].add_text("Getränke", gl.debug_font, (0,0,255))
		sc_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", gl.W-35-300, 35, 300, 530))
		sc_btns[-1].add_text("Importieren", gl.debug_font, (0,0,255))
		sc_btns[sc_pos].selected = True

	# input
	if io.read_input(io.BACK):		# if going back
		sc_active = False
		gl.prog_pos = 'm'
	elif io.read_input(io.NEXT):		# selecting a setting
		sc_active = False
		if sc_pos == 0:
			gl.prog_pos = 'sd'
		else:
			gl.prog_pos = 'si'
	elif io.read_input(io.LEFT):		# moving the selection
		sc_pos = 0
		sc_btns[0].selected = True
		sc_btns[1].selected = False
	elif io.read_input(io.RIGHT):
		sc_pos = 1
		sc_btns[0].selected = False
		sc_btns[1].selected = True

	# draw
	sc_background.draw()
	for i in sc_btns:
		i.draw()


	if sc_active == False:		# when leaving settings_choose
		sc_background = None
		sc_btns.clear()


# settings: setting drinks
sd_active = False

sd_background = None

sd_drinks_list = []
sd_first_drink = 0

sd_btn_list = []
sd_chosen_btn = 0
sd_n_visible_btn = 10

sd_plug_btn = None
sd_plug_num = 1

def settings_drink():
	global sd_active, sd_background, sd_drinks_list, sd_first_drink, sd_btn_list, sd_chosen_btn, sd_n_visible_btn, sd_plug_btn, sd_plug_num

	if sd_active == False:			# when entering drink settings
		sd_active = True
		sd_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")		# create background
		sd_background.start(repeat=True)

		# get recipes
		sd_drinks_list = drinks.get_drinks()
		sd_drinks_list.remove('cleaning_water')		# remove cleaning_water, as it is strictly set to plug 0
		sd_drinks_list.remove("None")				# put 'None' in first place
		sd_drinks_list.insert(0, "None")

		# create button list
		x, y = gl.W - int((3.5+0.1+0.25)*100), int(0.35*100)
		w, h = int(3.5*100), int(5.3*100/sd_n_visible_btn)
		for i in range(sd_n_visible_btn):
			sd_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
			y += h
		sd_btn_list[sd_chosen_btn].selected = True

		#create plug button
		sd_plug_btn = media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", gl.W-int(0.35*100)-h, int(0.35*100), h, h)
		sd_plug_btn.add_text(str(sd_plug_num), gl.standard_font, (0,0,255))
	
	# input
	if io.read_input(io.BACK):
		sd_active = False
		gl.prog_pos = 'sc'

	# selecting drink
	elif io.read_input(io.UP):
		if sd_chosen_btn == 0:
			sd_first_drink -= 1
			if sd_first_drink < 0:
				sd_first_drink = 0

		sd_btn_list[sd_chosen_btn].selected = False
		sd_chosen_btn -= 1
		if sd_chosen_btn < 0:
			sd_chosen_btn = 0
		sd_btn_list[sd_chosen_btn].selected = True


	elif io.read_input(io.DOWN):
		if sd_chosen_btn == sd_n_visible_btn-1:
			sd_first_drink += 1
			if sd_first_drink > len(sd_drinks_list) - sd_n_visible_btn:
				sd_first_drink = len(sd_drinks_list) - sd_n_visible_btn

		sd_btn_list[sd_chosen_btn].selected = False
		sd_chosen_btn += 1
		if sd_chosen_btn > sd_n_visible_btn-1:
			sd_chosen_btn = sd_chosen_btn-1
		sd_btn_list[sd_chosen_btn].selected = True

	# selecting plug
	elif io.read_input(io.LEFT):
		sd_plug_num -= 1
		if sd_plug_num < 1:
			sd_plug_num = 1
		# add text plug field
		sd_plug_btn.add_text(str(sd_plug_num), gl.standard_font, (0,0,255))
	elif io.read_input(io.RIGHT):
		sd_plug_num += 1
		if sd_plug_num > len(drinks.plugs)-1:
			sd_plug_num = len(drinks.plugs)-1
		# add text plug field
		sd_plug_btn.add_text(str(sd_plug_num), gl.standard_font, (0,0,255))

	# setting new drink to plug
	elif io.read_input(io.NEXT):
		drink = sd_btn_list[sd_chosen_btn].text
		if drink == "leer":
			drink = 'None'
		drinks.set_drink(sd_plug_num, drink)
		

	# add the drink names to the buttons
	for idx, btn in enumerate(sd_btn_list):
		text = sd_drinks_list[sd_first_drink+idx]
		if text == 'None':
			text = 'leer'
		btn.add_text(text, gl.standard_font, (0,0,255))

	# draw
	sd_background.draw()
	for i in sd_btn_list:
		i.draw()
	sd_plug_btn.draw()

	if sd_active == False:		# when leaving drink settings
		print("[UI SD] leavin' import settings")
		sd_background = None
		sd_drinks_list.clear()
		sd_btn_list.clear()
		sd_plug_btn = None
	
	if gl.show_debug:		# append debug info
		gl.debug_text.append("[UI SD] chosen_btn: " + str(sd_chosen_btn) + " first_drink: " + str(sd_first_drink) +  " chosen_drink: " + str(drinks.drinks[sd_first_drink+sd_chosen_btn]))
		t = "[UI SD] set drinks:"
		for idx, drink in enumerate(drinks.plugs):
			t += " " + str(idx) + ": " + str(drink) + "; "
		gl.debug_text.append(t)

# settings: import
si_active = False

si_background = None

si_recipe_list = []
si_first_recipe = 0

si_btn_list = []
si_chosen_btn = 0
si_n_visible_btn = 10

si_import_btn = None

def settings_import():
	global si_active, si_background, si_recipe_list, si_first_recipe, si_btn_list, si_chosen_btn, si_n_visible_btn, si_import_btn

	if si_active == False:			# when entering import settings
		si_active = True
		si_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")		# create background
		si_background.start(repeat=True)

		# get recipes
		si_recipe_list = drinks.get_recipes()

		# create button list
		x, y = int(0.25*100), int(0.35*100)
		w, h = int(3.5*100), int(5.3*100/si_n_visible_btn)
		for i in range(si_n_visible_btn):
			si_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
			y += h
		si_btn_list[si_chosen_btn].selected = True

		# create import button
		si_import_btn = media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", int(gl.W-(0.25+1)*100), 480, 100, 50)
		si_import_btn.add_text("Import", gl.standard_font, (0,0,255))

	# input
	if io.read_input(io.BACK):
		si_active = False
		gl.prog_pos = 'sc'

	elif io.read_input(io.UP) and si_import_btn.selected == False:
		if si_chosen_btn == 0:
			si_first_recipe -= 1
			if si_first_recipe < 0:
				si_first_recipe = 0

		si_btn_list[si_chosen_btn].selected = False
		si_chosen_btn -= 1
		if si_chosen_btn < 0:
			si_chosen_btn = 0
		si_btn_list[si_chosen_btn].selected = True


	elif io.read_input(io.DOWN) and si_import_btn.selected == False:
		if si_chosen_btn == si_n_visible_btn-1:
			si_first_recipe += 1
			if si_first_recipe > len(si_recipe_list) - si_n_visible_btn:
				si_first_recipe = len(si_recipe_list) - si_n_visible_btn

		si_btn_list[si_chosen_btn].selected = False
		si_chosen_btn += 1
		if si_chosen_btn > si_n_visible_btn-1:
			si_chosen_btn = si_chosen_btn-1
		si_btn_list[si_chosen_btn].selected = True

	elif io.read_input(io.RIGHT):
		si_import_btn.selected = True
		si_btn_list[si_chosen_btn].selected = False

	elif io.read_input(io.LEFT):
		si_import_btn.selected = False
		si_btn_list[si_chosen_btn].selected = True

	elif io.read_input(io.NEXT):
		if si_import_btn.selected:
			print("[UI SI] import recipe procedure started")
			success = drinks.import_recipe()
			if success:
				print("[UI SI] recipe succesfully imported")
				si_active = False
			else:
				print("[UI SI] an error occured during import")


		else:
			drinks.delete_recipe(si_first_recipe+si_chosen_btn)
			si_active = False

	
	# add the recipe names to the buttons
	for idx, btn in enumerate(si_btn_list):
		btn.add_text(si_recipe_list[si_first_recipe+idx], gl.standard_font, (0,0,255))

	# draw
	si_background.draw()
	for i in si_btn_list:
		i.draw()
	si_import_btn.draw()

	if si_active == False:		# when leaving import settings
		print("[UI SI] leavin' import settings")
		si_background = None
		si_recipe_list.clear()
		si_btn_list.clear()

	if gl.show_debug:		# append debug info
		gl.debug_text.append("[UI SI] chosen_btn: " + str(si_chosen_btn) + " first_recipe: " + str(si_first_recipe) +  " chosen_recipe: " + str(drinks.recipes[si_first_recipe+si_chosen_btn]))

""" ### CREDITS ### """
cr_active = False
cr_background = None
cr_text = None
def credits():
	global cr_active, cr_background, cr_text

	if cr_active == False: 		# whe entering credits
		cr_active = True
		cr_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")
		cr_background.start(repeat=True)
		cr_text = media_lib.TextField(0,8,gl.W, gl.H-8, gl.credits_text, gl.debug_font, (255,255,255), alignment=0)

	# input
	if io.read_input(io.BACK):
		cr_active = False

	# draw
	cr_background.draw()
	cr_text.draw()

	if cr_active == False:			# when leaving credits
		cr_background = None
		cr_text = None
		gl.prog_pos = gl.cr_prev_pos




""" ### SHUTDOWN ### """
def shutdown():
	print("STOPPING PROGRAM")
	if gl.os_is_linux:
		from subprocess import call
		call("sudo shutdown -h now", shell=True)
	gl.prog_active = False
