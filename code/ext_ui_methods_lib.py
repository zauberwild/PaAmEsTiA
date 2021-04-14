"""
this file include all methods for the user interface
"""

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
	gl.prog_pos = 'sc'		# DEL as soon as intro is needed again

	global intro_active, introduction_vid

	if intro_active == False:		# setup
		intro_active = True
		introduction_vid.start()			# start intro
	
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
	if io.read_input(io.UP):
		menu_pos -= 1
	if io.read_input(io.DOWN):
		menu_pos += 1

	# select menu item
	if io.read_input(io.NEXT):
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
def free_transition():
	gl.prog_pos = 'fc'



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
def recipe_transition():
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
def settings_transition():
	gl.prog_pos = 'sc'

s_active = False
s_background = None				# background for the settings

s_focus = 0					# focus on tab bar (0), on content (1), or selected something on content (2)

s_tab_pos = 1						# position / selected tab (set drinks, import, credits)
s_tabs = []

s_d_btn_pos = 0					# settings drinks buttons
s_d_buttons = []
s_d_ol_btn_pos = 0					# overlay for schoosing drink
s_d_ol_buttons = []
s_d_ol_rows = 0

s_i_btn_pos = 0
s_i_buttons = []

s_c_objects = []

def settings():
	global s_active, s_background, s_tab_pos, s_tabs, s_focus
	global s_d_btn_pos, s_d_buttons, s_d_ol_btn_pos, s_d_ol_buttons, s_d_ol_rows
	global s_c_objects

	if s_active == False:		# getting into settings
		s_active = True

		# start background video
		s_background = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")
		s_background.start(repeat=True)

		# adding tabs
		s_tabs.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 0,0, 64, 64))
		s_tabs[-1].add_text("<", gl.debug_font_big, (0,0,255))
		s_tabs.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 72, 0, 237, 64))
		s_tabs[-1].add_text("Getränke", gl.debug_font_big, (0,0,255))
		s_tabs.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 317, 0, 237, 64))
		s_tabs[-1].add_text("Import", gl.debug_font_big, (0,0,255))
		s_tabs.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 562, 0, 237, 64))
		s_tabs[-1].add_text("Credits", gl.debug_font_big, (0,0,255))
		s_tab_pos = 1
		s_tabs[s_tab_pos].selected = True

		# button for settting the drinks
		s_d_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 64, 400, 237, 64))
		s_d_buttons[-1].add_text(drinks.plugs[1], gl.debug_font_big, (0,0,255))
		s_d_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 128, 285, 237, 64))
		s_d_buttons[-1].add_text(drinks.plugs[2], gl.debug_font_big, (0,0,255))
		s_d_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 282, 180, 237, 64))
		s_d_buttons[-1].add_text(drinks.plugs[3], gl.debug_font_big, (0,0,255))
		s_d_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 435, 285, 237, 64))
		s_d_buttons[-1].add_text(drinks.plugs[4], gl.debug_font_big, (0,0,255))
		s_d_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 499, 400, 237, 64))
		s_d_buttons[-1].add_text(drinks.plugs[5], gl.debug_font_big, (0,0,255))
		s_d_buttons[s_d_btn_pos].selected = True

		w, h = 238, 32
		x, y = gl.W/4-w/2, 64+8
		for i in drinks.drinks:
			if i != "cleaning_water":
				s_d_ol_buttons.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
				t=i
				if t == 'None':
					t = 'leer'
				s_d_ol_buttons[-1].add_text(t, gl.debug_font, (0,0,255))
				y += h + 4

				if y+h > gl.H:
					y = 64+8
					x += gl.W/2
					if s_d_ol_rows != 0:
						s_d_ol_rows = min(len(s_d_ol_buttons), s_d_ol_rows)
					else:
						s_d_ol_rows = len(s_d_ol_buttons)
		s_d_ol_buttons[s_d_ol_btn_pos].selected = True


		# objects for the credits
		s_c_objects.append(media_lib.TextField(0,64+8,gl.W, gl.H-(64+8), gl.credits_text, gl.debug_font, (255,255,255), alignment=0))
			


	""" logic and input """
	if s_focus >= 1:					# if focus on content
		if io.read_input(io.BACK):		# going back to tab bar
			s_focus = 0

		# setting drinks
		if s_tab_pos == 1:
			if s_focus == 1:
				if io.read_input(io.LEFT):				# going left or right between the drinks
					s_d_buttons[s_d_btn_pos].selected = False
					s_d_btn_pos -= 1
					if s_d_btn_pos < 0:
						s_d_btn_pos = 0
					s_d_buttons[s_d_btn_pos].selected = True
				if io.read_input(io.RIGHT):
					s_d_buttons[s_d_btn_pos].selected = False
					s_d_btn_pos += 1
					if s_d_btn_pos > len(s_d_buttons)-1:
						s_d_btn_pos = len(s_d_buttons)-1
					s_d_buttons[s_d_btn_pos].selected = True
				if io.read_input(io.NEXT):
					s_focus = 2

			elif s_focus == 2:
				if io.read_input(io.BACK):
					s_focus = 1
				if io.read_input(io.UP):				# going through drink selection
					s_d_ol_buttons[s_d_ol_btn_pos].selected = False
					s_d_ol_btn_pos -= 1
					if s_d_ol_btn_pos < 0:
						s_d_ol_btn_pos = 0
					s_d_ol_buttons[s_d_ol_btn_pos].selected = True
				if io.read_input(io.DOWN):
					s_d_ol_buttons[s_d_ol_btn_pos].selected = False
					s_d_ol_btn_pos += 1
					if s_d_ol_btn_pos > len(s_d_ol_buttons)-1:
						s_d_ol_btn_pos = len(s_d_ol_buttons)-1
					s_d_ol_buttons[s_d_ol_btn_pos].selected = True
				if io.read_input(io.LEFT):
					s_d_ol_buttons[s_d_ol_btn_pos].selected = False
					s_d_ol_btn_pos -= s_d_ol_rows
					if s_d_ol_btn_pos < 0:
						s_d_ol_btn_pos = 0
					s_d_ol_buttons[s_d_ol_btn_pos].selected = True
				if io.read_input(io.RIGHT):
					s_d_ol_buttons[s_d_ol_btn_pos].selected = False
					s_d_ol_btn_pos += s_d_ol_rows
					if s_d_ol_btn_pos > len(s_d_ol_buttons)-1:
						s_d_ol_btn_pos = len(s_d_ol_buttons)-1
					s_d_ol_buttons[s_d_ol_btn_pos].selected = True
				if io.read_input(io.NEXT):
					s_focus = 1
					drink = s_d_ol_buttons[s_d_ol_btn_pos].text
					if drink == 'leer':
						drink = 'None'
					drinks.set_drink(s_d_btn_pos+1, drink)
					s_d_buttons[s_d_btn_pos].text = s_d_ol_buttons[s_d_ol_btn_pos].text
					print("[UI SD]", "setting drink", drinks.plugs[s_d_btn_pos+1], "on plug", s_d_btn_pos+1)


		# credits
		elif s_tab_pos == 3:
			pass

	else:						# if focus on tab_bar
		if io.read_input(io.LEFT):				# going left or right on the tab bar
			s_tabs[s_tab_pos].selected = False
			s_tab_pos -= 1
			if s_tab_pos < 0:
				s_tab_pos = 0
			s_tabs[s_tab_pos].selected = True
		if io.read_input(io.RIGHT):
			s_tabs[s_tab_pos].selected = False
			s_tab_pos += 1
			if s_tab_pos > len(s_tabs)-1:
				s_tab_pos = len(s_tabs)-1
			s_tabs[s_tab_pos].selected = True
		
		if io.read_input(io.BACK) or (io.read_input(io.NEXT) and s_tab_pos == 0):			# if leaving the settings
			s_active = False
			gl.prog_pos = 'm'

		if io.read_input(io.NEXT) and s_tab_pos != 0:			# if selecting a tab
			s_focus = 1
			

	""" drawing """
	s_background.draw()
	for i in s_tabs:
		i.draw()

	if s_tab_pos <= 1:
		if s_focus <= 1:
			for i in s_d_buttons:
				i.draw()
		if s_focus == 2:
			for i in s_d_ol_buttons:
				i.draw()
	elif s_tab_pos == 2:
		pass
	elif s_tab_pos == 3:
		for i in s_c_objects:
			i.draw()


	""" leaving settings """
	if s_active == False:
		s_background = None
		s_tabs.clear()
		s_d_buttons.clear()
		s_d_ol_buttons.clear()
		s_c_objects.clear()

	""" debug info """
	if gl.show_debug:
		gl.debug_text.append("s_focus: " + str(s_focus) + "; s_tab_pos: " + str(s_tab_pos))



""" ### SHUTDOWN ### """
def shutdown():
	print("STOPPING PROGRAM")
	if gl.os_is_linux:
		from subprocess import call
		call("sudo shutdown -h now", shell=True)
	gl.prog_active = False
