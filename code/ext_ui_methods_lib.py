"""
this file include all methods for the user interface
"""

#from tkinter.constants import TRUE
#from numpy import true_divide
import globals as gl
import io_lib as io
import media_lib
import drinks_lib as drinks

""" ### ### SETUP / LOOP ### ### """
""" actions that need to be executed once on startup are here 
	This includes object creation, reading files in, etc.
"""

file = open(gl.gen_path + "/src/drinks")			# DEL i guess
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

def end_loop():
	""" actions that need to be executed every loop AT THE END are here. """
	# draw and update notifications
	for i in gl.notifications:
		i.update()



""" ### ### INTRO / MAIN MENU ### ### """
intro_active = False

introduction_vid = None		# saves the video ofr the intro

def intro():
	global intro_active, introduction_vid

	gl.prog_pos = 'm'		# DEL as soon as intro is needed again

	if intro_active == False:		# setup
		intro_active = True
		introduction_vid = media_lib.Video(gl.gen_path + "/src/media/intro/intro.mp4")
		introduction_vid.start()			# start intro
	
	introduction_vid.draw()				# draw intro

	if introduction_vid.test_for_last_frame() or intro_active == False:			# test if intro is ending
		intro_active = False
		introduction_vid = None
		gl.prog_pos = 'm'


menu_background = None
menu_active = False
menu_btns = []				# saves the buttons of the main menu
menu_pos_x = 1				# postion of the buttons
menu_pos_y = 0

def main_menu():
	global menu_background, menu_active, menu_btns, menu_pos_x, test_recipe, menu_pos_y
	
	if menu_active == False:			# setup
		menu_active = True

		# background
		menu_background = media_lib.Image(gl.gen_path + "/src/media/background.jpeg", 0, 0, gl.W, gl.H)

		# creating the buttons for the main menu
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/media/main_menu/", "settings.png", "settings_sel.png", "settings.png", 48, 48, 197, 439))
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/media/main_menu/", "recipes.png", "recipes_sel.png", "recipes.png", 261, 13, 279, 484))
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/media/main_menu/", "free.png", "free_sel.png", "free.png", 557, 48, 197, 439))
		menu_btns.append(media_lib.Button(gl.gen_path + "/src/media/main_menu/", "quit.png", "quit_sel.png", "quit.png", 274, 511, 250, 77))
		menu_btns[1].selected = True
		menu_pos_x = 1				# postion of the buttons
		menu_pos_y = 0
	
	# input
	if io.read_input(io.UP):
		menu_pos_y = 0
		menu_btns[menu_pos_x].selected = True
		menu_btns[3].selected = False
	elif io.read_input(io.DOWN):
		menu_pos_y = 1
		menu_btns[menu_pos_x].selected = False
		menu_btns[3].selected = True
	elif io.read_input(io.LEFT) and menu_pos_y == 0:
		menu_btns[menu_pos_x].selected = False
		menu_pos_x -= 1
		if menu_pos_x < 0:
			menu_pos_x = 0
		menu_btns[menu_pos_x].selected = True
	elif io.read_input(io.RIGHT) and menu_pos_y == 0:
		menu_btns[menu_pos_x].selected = False
		menu_pos_x += 1
		if menu_pos_x > 2:
			menu_pos_x = 2
		menu_btns[menu_pos_x].selected = True

	elif io.read_input(io.NEXT):
		menu_active = False
		if menu_pos_y == 0:
			if menu_pos_x == 0:
				gl.prog_pos = 'sc'
			elif menu_pos_x == 1:
				gl.prog_pos = 'rc'
			elif menu_pos_x == 2:
				gl.prog_pos = 'fc'
		elif menu_pos_y == 1:
			gl.prog_pos = 'q'

	# draw
	menu_background.draw()

	# for each button in list
	for btn in menu_btns:
		btn.draw()

	# exiting the main menu
	if menu_active == False:
		menu_background = None
		menu_btns.clear()

	# append debug information
	if gl.show_debug:
		gl.debug_text.append("menu_pos_x: " + str(menu_pos_x))


""" ### ### FREE MIXING ### ### """

fc_active = False			# controls if free_choose is active or not
fc_background = None		# saves the background video
fc_buttons = []				# saves the buttons at the buttom
fc_bars = []				# saves the (progress) bars
fc_sum_image = None
fc_sum_text = None			# saves the textfield showing the sum of all drinks

fc_pos = 1					# position on the menu (0: go back, 1-5: drinks, 6: next)
fc_values = [0,0,0,0,0]		# saves values for the drinks

def free_choose():
	global fc_active, fc_background, fc_buttons, fc_bars, fc_pos, fc_values, fc_sum_text, fc_sum_image
	
	# entering free_choose
	if fc_active == False:
		fc_active = True
		# set video background
		fc_background = media_lib.Image(gl.gen_path + "/src/media/background.jpeg", 0, 0, gl.W, gl.H)

		# set buttons
		# button: go back
		fc_buttons.append(media_lib.Button(gl.gen_path + "/src/media/free/", "back.png", "back_sel.png", "back.png", 47, 515, 64, 50))
		

		# buttons with the drinks and bars
		x = [57, 57, 290, 523, 523]
		y = [115] * 5
		w = [221] * 5
		h = [377] * 5
		img = ["tower_1.png", "tower_2.png", "tower_3.png", "tower_4.png", "tower_5.png"]
		img_sel = ["tower_1_sel.png", "tower_2_sel.png", "tower_3_sel.png", "tower_4_sel.png", "tower_5_sel.png"]
		bar = ["tower_1/", "tower_2/", "tower_3/", "tower_4/", "tower_5/"]
		for i in range(5):
			fc_buttons.append(media_lib.Button(gl.gen_path + "/src/media/free/", img[i], img_sel[i], img[i], x[i], y[i], w[i], h[i]))
			fc_bars.append(media_lib.Bar(gl.gen_path + "/src/media/free/" + bar[i], x[i], y[i], w[i], h[i]))

		# button: next
		fc_buttons.append(media_lib.Button(gl.gen_path + "/src/media/free/", "next.png", "next_sel.png", "next.png", 704, 515, 64, 50))

		fc_buttons[fc_pos].selected = True

		# textfield for sum
		fc_sum_image = media_lib.Image(gl.gen_path + "/src/media/free/sum_bg.png", 153, 17, 495, 69)
		fc_sum_text = media_lib.Bar(gl.gen_path + "/src/media/free/sum/", 345, 35, 112, 39)

	""" logic / input """
	# go left or right
	if io.read_input(io.LEFT):
		fc_buttons[fc_pos].selected = False
		fc_pos -= 1
		if fc_pos < 0:								# lower boundary
			fc_pos = 0
		fc_buttons[fc_pos].selected = True
	if io.read_input(io.RIGHT):
		fc_buttons[fc_pos].selected = False
		fc_pos += 1
		if fc_pos > len(fc_buttons)-1:				# upper boundary
			fc_pos = len(fc_buttons)-1
		fc_buttons[fc_pos].selected = True

	# raising / lowering values
	interval = 10			# interval, by which the values will be lowered/raised
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

		fc_sum_text.set_state(sum_values)			# update sum value


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
				text = str(drinks.plugs[idx+1]) + "," + str(val)				# prepare text (idx+1, because the first one would be cleaning_water)
				file.write(text+"\n")											# add to file with name and amount
		file.close()															# close file

		drinks.start_mixing("free_mixed_recipe")								# start the micing procedure with the freshly written file

		fc_active = False				# also, leave this menu
		gl.prog_pos = 'fo'				# and go to free_output

	""" draw """
	fc_background.draw()

	fc_sum_image.draw()
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
		fc_sum_image = None
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
		fo_background = media_lib.Video(gl.gen_path + "/src/media/loading.mp4")
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
rc_visible_n = 9			# number of visible items
rc_btns = []				# list holding the recipes buttons
rc_btn_size = (388, 47)			# size of buttons
rc_btn_size_sel = (404, 56)
rc_spacing = (12, 7)			# spacing between little button , spacing between big and little buttons
rc_x_offset = 16
rc_pos = 0					# position of selection in complete recipe list
rc_visible_pos = 0			# position in visible part

rc_recipes = []				# list of all recipes, sorted after availability, than alphabetically

rc_marker = []				# list holding markers

rc_standard_file = "/src/media/background.jpeg"	# standard background
rc_background = None		# video in the background

rc_stage = 0				# 0: show all recipes; 1: show info of selected recipe (-1: go back; 2: mix recipe)
rc_info_textfield = None	# holds a textfield as soon stage is set to showing info
rc_info_btns = []			# holds all objects for info screen

def recipe_choose():
	global rc_active, rc_btns, rc_pos, rc_visible_pos, rc_spacing, rc_x_offset, rc_recipes, rc_stage, rc_marker, rc_standard_file, rc_background, rc_info_textfield, rc_info_btns, rc_btn_size, rc_btn_size_sel

	# entering the menu
	if rc_active == False:
		rc_active = True

		# filling recipe list (first all available recipes, then the unavailable ones)
		list_available = drinks.get_recipes(available=True)
		list_available.sort()
		list_unavailable = drinks.get_recipes(available=False)
		list_unavailable.sort()
		rc_recipes = list_available + list_unavailable

		# creating background
		rc_background = media_lib.Image(gl.gen_path + rc_standard_file, 0, 0, gl.W, gl.H)

		# creating buttons
		height = 44
		rc_btns.clear()
		for i in range(rc_visible_n):
			if i == rc_visible_pos:
				# selected button
				rc_btns.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "btn_sel.png", "btn_sel.png", "btn_sel.png", 90, height, rc_btn_size_sel[0], rc_btn_size_sel[1]))
				height += rc_btn_size_sel[1] + rc_spacing[1]
			else:
				# other buttons
				rc_btns.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "btn.png", "btn.png", "btn.png", 90 + rc_x_offset, height, rc_btn_size[0], rc_btn_size[1]))
				height += rc_btn_size[1] + rc_spacing[0]
				if i+1 == rc_visible_pos:
					height -= rc_spacing[0]-rc_spacing[1]

		# creating marker
		rc_marker.clear()
		rc_marker.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "marker_up_sel.png", "marker_up_sel.png", "marker_up.png", 283, 7, 35, 30))
		rc_marker.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "marker_down_sel.png", "marker_down_sel.png", "marker_down.png", 281, 563, 35, 30))
		rc_marker[1].set_size(y=rc_btns[-1].y + rc_btns[-1].height + 7)


	""" input """
	# go up or down
	if rc_stage == 0:					# only if in list mode
		if io.read_input(io.UP):
			rc_visible_pos -= 1
			rc_pos -= 1
			if rc_visible_pos < 0:
				rc_visible_pos = 0
		if io.read_input(io.DOWN):
			rc_visible_pos += 1
			rc_pos += 1
			if rc_visible_pos > rc_visible_n-1:
				rc_visible_pos = rc_visible_n-1
		if io.read_input(io.UP) or io.read_input(io.DOWN):
			height = 44
			rc_btns.clear()
			for i in range(rc_visible_n):
				if i == rc_visible_pos:
					# selected button
					rc_btns.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "btn_sel.png", "btn_sel.png", "btn_sel.png", 90, height, rc_btn_size_sel[0], rc_btn_size_sel[1]))
					height += rc_btn_size_sel[1] + rc_spacing[1]
				else:
					# other buttons
					rc_btns.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "btn.png", "btn.png", "btn.png", 90 + rc_x_offset, height, rc_btn_size[0], rc_btn_size[1]))
					height += rc_btn_size[1] + rc_spacing[0]
					if i+1 == rc_visible_pos:
						height -= rc_spacing[0]-rc_spacing[1]
				rc_marker[1].set_size(y=rc_btns[-1].y + rc_btns[-1].height + 7)

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
	
	# menu boundaries
	# complete list
	if rc_pos < 0:
		rc_pos = 0
	elif rc_pos > len(rc_recipes)-1:
		rc_pos = len(rc_recipes)-1
	
	# moving menu / setting correct text
	a = rc_pos - rc_visible_pos 		# first visible item
	for btn in rc_btns:
		btn.add_text(rc_recipes[a], gl.standard_font, gl.text_color_1, 1)
		a += 1

	# control marker
	# upper marker
	if rc_btns[rc_visible_pos].text == rc_recipes[0]:	# if first item in recipe-list is visible -> we are on the top of the list
		rc_marker[0].disabled = True
	else:
		rc_marker[0].disabled = False
	# lower marker
	if rc_btns[rc_visible_pos].text == rc_recipes[-1]:	# if last item in recipe-list is visible -> we are on the bottom of the list
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
		rc_info_textfield = media_lib.TextField(98, 107, 396, 203, text, gl.standard_font_small, gl.text_color_1, alignment=1)
		rc_info_textfield.add_background(gl.gen_path + "/src/media/recipe/info_textfield.png")
		# creating info objects
		a = drinks._test_availability(chosen_recipe)
		rc_info_btns.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "mix.png", "mix_sel.png", "mix.png", 635, 509, 131, 45, selected=a))		# mix button
		rc_info_btns.append(media_lib.Button(gl.gen_path + "/src/media/recipe/", "info_recipe.png", "mix_sel.png", "mix.png", 90, 44, 404, 56))		# recipe name
		rc_info_btns[-1].add_text(chosen_recipe, gl.standard_font, gl.text_color_1, hor_alignment=1)
		
	# disabling info
	if rc_stage == 0 and rc_info_textfield:
		rc_info_textfield = None
		rc_info_btns.clear()
			
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

	""" draw """
	rc_background.draw()
	if rc_stage == 0:					# list mode
		for i in rc_btns:
			i.draw()
		for i in rc_marker:
			i.draw()
	elif rc_stage == 1:					# info mode
		rc_info_textfield.draw()
		for i in rc_info_btns:
			i.draw()

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
							"; rc_stage: " + str(rc_stage) + 
							"; chosen_recipe: " + str(chosen_recipe))

ro_active = False
ro_background = None			# background
def recipe_output():
	global ro_active, ro_background

	if not ro_active:		# if first entering recipe output
		ro_active = True
		ro_background = media_lib.Video(gl.gen_path + "/src/media/loading.mp4")
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
sc_pos = 0						# position / selected button

def settings_choose():
	global sc_active, sc_background, sc_btns, sc_pos

	if sc_active == False:		# when entering settings_choose
		sc_active = True
		sc_background = media_lib.Video(gl.gen_path + "/src/props/intro.mp4")		# create background
		sc_background.start(repeat=True)

		# create buttons
		sc_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 14, 10, 326, 582))
		sc_btns[-1].add_text("Getränke", gl.debug_font, (0,0,255))		# DEL src rdy
		sc_btns.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 461, 10, 326, 582))
		sc_btns[-1].add_text("Importieren", gl.debug_font, (0,0,255))	# DEL src rdy
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

sd_drinks_list = []				# contains all drinks
sd_first_drink = 0

sd_btn_list = []				# contains all buttons
sd_chosen_btn = 0
sd_n_visible_btn = 9
sd_btn_list_cords = (206, 43, 388, 47)		# x, y, w, h
sd_btn_list_cords_sel = (188, 43, 366, 56)		# x, y, w, h
sd_spacing = rc_spacing

sd_marker = []				# list holding markers

sd_plug_img = None			# small image indicating selected plug
sd_plug_img_name = ["cleaning_water can't be changed", "prop_1.png", "prop_2.png", "prop_3.png", "prop_4.png", "prop_5.png"]
sd_plug_num = 1
sd_plug_img_cords = [537, 43, 92, 56]				# x, y, w, h
sd_plug_img_y_pos = []								# height for every button / possible place

def settings_drink():
	global sd_active, sd_background, sd_drinks_list, sd_spacing, sd_btn_list_cords_sel, sd_plug_img_y_pos, sd_first_drink, sd_btn_list, sd_chosen_btn, sd_n_visible_btn, sd_marker, sd_plug_img, sd_plug_img_name, sd_plug_num, sd_plug_img_cords, sd_btn_list_cords

	if sd_active == False:			# when entering drink settings
		sd_active = True
		sd_background = media_lib.Video(gl.gen_path + "/src/props/intro.mp4")		# create background
		sd_background.start(repeat=True)

		# get recipes
		sd_drinks_list = drinks.get_drinks()
		sd_drinks_list.remove('cleaning_water')		# remove cleaning_water, as it is already permanently set to plug 0
		sd_drinks_list.remove("None")				# put 'None' in first place
		sd_drinks_list.insert(0, "None")

		# create button list
		x, y = sd_btn_list_cords[0], sd_btn_list_cords[1]
		w, h = sd_btn_list_cords[2], sd_btn_list_cords[3]
		for i in range(sd_n_visible_btn):
			sd_plug_img_y_pos.append(y)
			if i == sd_chosen_btn:
				l_x = sd_btn_list_cords_sel[0]
				l_w, l_h = sd_btn_list_cords_sel[2], sd_btn_list_cords_sel[3]
				sd_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", l_x, y, l_w, l_h))
				y += l_h + sd_spacing[1]
			else:
				sd_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
				y += h + sd_spacing[0]
				if i+1 == sd_chosen_btn:
						y -= sd_spacing[0]-sd_spacing[1]
		sd_btn_list[sd_chosen_btn].selected = True

		# create marker
		sd_marker.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_green.png", "prop_white.png", "prop_tri_grey.png", 383, 6, 35, 30, rotation=180))
		sd_marker.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_green.png", "prop_white.png", "prop_tri_grey.png", 383, 563, 35, 30))

		#create plug image
		sd_plug_img = media_lib.Image(gl.gen_path + "/src/props/" + sd_plug_img_name[sd_plug_num], sd_plug_img_cords[0], sd_plug_img_cords[1], sd_plug_img_cords[2], sd_plug_img_cords[3])
	
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

		# menu boundaries
		sd_chosen_btn -= 1
		if sd_chosen_btn < 0:
			sd_chosen_btn = 0
		sd_btn_list[sd_chosen_btn].selected = True
	elif io.read_input(io.DOWN):
		if sd_chosen_btn == sd_n_visible_btn-1:
			sd_first_drink += 1
			if sd_first_drink > len(sd_drinks_list) - sd_n_visible_btn:
				sd_first_drink = len(sd_drinks_list) - sd_n_visible_btn

		# menu boundaries
		sd_chosen_btn += 1
		if sd_chosen_btn > sd_n_visible_btn-1:
			sd_chosen_btn = sd_chosen_btn-1
	
	if io.read_input(io.UP) or io.read_input(io.DOWN):
		sd_btn_list.clear()
		x, y = sd_btn_list_cords[0], sd_btn_list_cords[1]
		w, h = sd_btn_list_cords[2], sd_btn_list_cords[3]
		for i in range(sd_n_visible_btn):
			if i == sd_chosen_btn:
				l_x = sd_btn_list_cords_sel[0]
				l_w, l_h = sd_btn_list_cords_sel[2], sd_btn_list_cords_sel[3]
				sd_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", l_x, y, l_w, l_h))
				y += l_h + sd_spacing[1]
			else:
				sd_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
				y += h + sd_spacing[0]
				if i+1 == sd_chosen_btn:
					y -= sd_spacing[0]-sd_spacing[1]

		sd_btn_list[sd_chosen_btn].selected = True
		l_y = sd_btn_list[sd_chosen_btn].y
		sd_plug_img_cords[1] = l_y
		sd_plug_img = sd_plug_img = media_lib.Image(gl.gen_path + "/src/props/" + sd_plug_img_name[sd_plug_num], sd_plug_img_cords[0], l_y, sd_plug_img_cords[2], sd_plug_img_cords[3])

	# selecting plug
	elif io.read_input(io.LEFT):
		sd_plug_num -= 1
		if sd_plug_num < 1:
			sd_plug_num = 1
		# add text plug field
		sd_plug_img = media_lib.Image(gl.gen_path + "/src/props/" + sd_plug_img_name[sd_plug_num], sd_plug_img_cords[0], sd_plug_img_cords[1], sd_plug_img_cords[2], sd_plug_img_cords[3])
	elif io.read_input(io.RIGHT):
		sd_plug_num += 1
		if sd_plug_num > len(drinks.plugs)-1:
			sd_plug_num = len(drinks.plugs)-1
		# add text plug field
		sd_plug_img = media_lib.Image(gl.gen_path + "/src/props/" + sd_plug_img_name[sd_plug_num], sd_plug_img_cords[0], sd_plug_img_cords[1], sd_plug_img_cords[2], sd_plug_img_cords[3])

	# setting new drink to plug
	elif io.read_input(io.NEXT):
		drink = sd_btn_list[sd_chosen_btn].text
		drinks.set_drink(sd_plug_num, drink)
		notification_text = str(sd_plug_num) + " set to " + str(drink)
		if drink == 'None':
			notification_text = str(sd_plug_num) + " set clear"
		gl.notifications.append(media_lib.Notification(notification_text))
		

	# add the drink names to the buttons
	for idx, btn in enumerate(sd_btn_list):
		text = sd_drinks_list[sd_first_drink+idx]
		btn.add_text(text, gl.standard_font, (0,0,255))

	# control marker
	# upper marker
	if sd_btn_list[0].text == sd_drinks_list[0]:	# if first item in recipe-list is visible -> we are on the top of the list
		sd_marker[0].disabled = True
	else:
		sd_marker[0].disabled = False
	# lower marker
	if sd_btn_list[-1].text == sd_drinks_list[-1]:	# if last item in recipe-list is visible -> we are on the bottom of the list
		sd_marker[1].disabled = True
	else:
		sd_marker[1].disabled = False

	# draw
	sd_background.draw()
	for i in sd_btn_list:
		i.draw()
	for i in sd_marker:
		i.draw()
	sd_plug_img.draw()

	if sd_active == False:		# when leaving drink settings
		print("[UI SD] leaving import settings")
		sd_background = None
		sd_drinks_list.clear()
		sd_btn_list.clear()
		sd_plug_img = None
		sd_marker.clear()
		sd_plug_img_y_pos.clear()
	
	if gl.show_debug:		# append debug info
		gl.debug_text.append("[UI SD] chosen_btn: " + str(sd_chosen_btn) + " first_drink: " + str(sd_first_drink) +  " chosen_drink: " + str(drinks.drinks[sd_first_drink+sd_chosen_btn]))
		t = "[UI SD] set drinks:"
		for idx, drink in enumerate(drinks.plugs):
			t += " " + str(idx) + ": " + str(drink) + "; "
		gl.debug_text.append(t)

# settings: import
si_active = False

si_background = None		# stores the background

si_recipe_list = []			# stores the recipes
si_first_recipe = 0			# stores the number of the first shown recipe

si_btn_list = []			# stores the Button objects
si_chosen_btn = 0			# stores the chosen Button
si_n_visible_btn = 9		# number of visible Buttons
si_btns_cords = (104, 43, 393, 47)		# x, y, w, h
si_btns_cords_sel = (87, 43, 409, 56)		# x, y, w, h
si_spacing = rc_spacing		# spacing between buttons

si_marker = []				# list holding markers

si_import_btn = None		# the import button in the bottom-right corner

def settings_import():
	global si_active, si_background, si_recipe_list, si_first_recipe, si_btn_list, si_chosen_btn, si_n_visible_btn, si_import_btn, si_marker, si_btns_cords, si_spacing, si_btns_cords_sel

	if si_active == False:			# when entering import settings
		si_active = True
		si_background = media_lib.Video(gl.gen_path + "/src/props/intro.mp4")		# create background
		si_background.start(repeat=True)

		# get recipes
		si_recipe_list = drinks.get_recipes()

		# create button list
		x, y = si_btns_cords[0], si_btns_cords[1]
		w, h = si_btns_cords[2], si_btns_cords[3]
		for i in range(si_n_visible_btn):
			if i == si_chosen_btn:
				l_x = si_btns_cords_sel[0]
				l_w, l_h = si_btns_cords_sel[2], si_btns_cords_sel[3]
				si_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", l_x, y, l_w, l_h))
				y += l_h + si_spacing[1]
			else:
				si_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
				y += h + si_spacing[0]
				if i+1 == si_chosen_btn:
					y -= si_spacing[0]-si_spacing[1]

		si_btn_list[si_chosen_btn].selected = True

		# create marker
		si_marker.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_green.png", "prop_white.png", "prop_tri_grey.png", 283, 6, 35,30, rotation=180))
		si_marker.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_tri_green.png", "prop_white.png", "prop_tri_grey.png", 283, 563, 35, 30))

		# create import button
		si_import_btn = media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", 635, 510, 131, 45)
		si_import_btn.add_text("Import", gl.standard_font, (0,0,255))

	# input
	if io.read_input(io.BACK):
		si_active = False
		gl.prog_pos = 'sc'

	elif io.read_input(io.UP) and si_import_btn.selected == False:		# moving up and down in the list
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

	if (io.read_input(io.DOWN) or io.read_input(io.UP)) and si_import_btn.selected == False:
		si_btn_list.clear()
		x, y = si_btns_cords[0], si_btns_cords[1]
		w, h = si_btns_cords[2], si_btns_cords[3]
		for i in range(si_n_visible_btn):
			if i == si_chosen_btn:
				l_x = si_btns_cords_sel[0]
				l_w, l_h = si_btns_cords_sel[2], si_btns_cords_sel[3]
				si_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", l_x, y, l_w, l_h))
				y += l_h + si_spacing[1]
			else:
				si_btn_list.append(media_lib.Button(gl.gen_path + "/src/props/", "prop_white.png", "prop_green.png", "prop_grey.png", x, y, w, h))
				y += h + si_spacing[0]
				if i+1 == si_chosen_btn:
					y -= si_spacing[0]-si_spacing[1]

		si_btn_list[si_chosen_btn].selected = True

	elif io.read_input(io.RIGHT):							# switch to import button
		si_import_btn.selected = True
		si_btn_list[si_chosen_btn].selected = False

	elif io.read_input(io.LEFT):							# switch to recipe list
		si_import_btn.selected = False
		si_btn_list[si_chosen_btn].selected = True

	elif io.read_input(io.NEXT):								# pressing next
		if si_import_btn.selected:								# if currently focusing the import-button
			print("[UI SI] import recipe procedure started")		# start recipe import
			success = drinks.import_recipe()
			if success:
				print("[UI SI] recipe successfully imported")
				si_active = False
				notification_text = "recipe successfully imported"
			else:
				print("[UI SI] an error occurred during import")
				notification_text = "An error occurred during import"

		else:													# if currently focusing somewhere on the list
			success = drinks.delete_recipe(si_first_recipe+si_chosen_btn)		# delete the chosen recipe (if possible)
			si_active = False
			if success:
				notification_text = "successfully deleted recipe"
			else:
				notification_text = "couldn't delete recipe, recipe is immutable"
		
		gl.notifications.append(media_lib.Notification(notification_text))

	# add the recipe names to the buttons
	for idx, btn in enumerate(si_btn_list):
		btn.add_text(si_recipe_list[si_first_recipe+idx], gl.standard_font, (0,0,255))

	# control marker
	# upper marker
	if si_btn_list[0].text == si_recipe_list[0]:	# if first item in recipe-list is visible -> we are on the top of the list
		si_marker[0].disabled = True
	else:
		si_marker[0].disabled = False
	# lower marker
	if si_btn_list[-1].text == si_recipe_list[-1]:	# if last item in recipe-list is visible -> we are on the bottom of the list
		si_marker[1].disabled = True
	else:
		si_marker[1].disabled = False

	# draw
	si_background.draw()
	for i in si_btn_list:
		i.draw()
	for i in si_marker:
		i.draw()
	si_import_btn.draw()

	if si_active == False:		# when leaving import settings
		print("[UI SI] leaving import settings")
		si_background = None
		si_recipe_list.clear()
		si_btn_list.clear()
		si_marker.clear()

	if gl.show_debug:		# append debug info
		gl.debug_text.append("[UI SI] chosen_btn: " + str(si_chosen_btn) + " first_recipe: " + str(si_first_recipe) +  " chosen_recipe: " + str(drinks.recipes[si_first_recipe+si_chosen_btn]))

""" ### CREDITS ### """
cr_active = False
cr_background = None			# stores background
cr_text = None					# stores the textfield
def credits():
	global cr_active, cr_background, cr_text

	if cr_active == False: 		# when entering credits
		cr_active = True
		# create objects
		cr_background = media_lib.Video(gl.gen_path + "/src/props/intro.mp4")
		cr_background.start(repeat=True)
		cr_text = media_lib.TextField(0,8,gl.W, gl.H-8, gl.credits_text, gl.standard_font, (255,255,255), alignment=0)

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

	if gl.show_debug:
		gl.debug_text.append("prev prog_pos: " + gl.cr_prev_pos)




""" ### SHUTDOWN ### """
def shutdown():
	print("STOPPING PROGRAM")
	if gl.os_is_linux:
		from subprocess import call							# sending the shutdown command for linux
		call("sudo shutdown -h now", shell=True)
	gl.prog_active = False									# on any other machine, simply stop the program
