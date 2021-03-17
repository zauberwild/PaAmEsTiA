"""
contains the recipe-class and drink-class
"""

# imports
import globals as gl
import io_lib as io
import os
import time

""" ### PATHS ### """
dir_recipes = gl.gen_path + "/src/recipes/"					# path to the recipe-directory

""" ### STORAGE ### """
plugs = ["cleaning_water", "", "", "", "", "", ""]			# stores the drinks plugged in

drinks = []													# stores the available drinks to choose from

recipes = []												# stores all recipes that could be found in the recipe folder

""" variables for mixing """
is_mixing = False				# stores, if currently a recipe is mixing
recipe_step = 0					# stores the current step
commands = []					# compiled command lines
finishing_time = 0				# precalculated time, when the timer will be done


""" ### SETUP ### """
# this part will run once, as soon this file is imported somewhere

# look for drinks
file1 = open(gl.gen_path + "/src/drinks", 'r')			# open file
drinks = file1.readlines()								# save lines as a list
file1.close()

for idx, i in enumerate(drinks):						# remove trailing newline characters
		if drinks[idx].endswith('\n'):
			drinks[idx] = drinks[idx][:-1]
drinks.sort()

# look for recipes
for filename in os.listdir(gl.gen_path + "/src/recipes"):
	recipes.append(filename)
recipes.sort()

""" ### TEST AVAILABILITY ### """
def _test_availability(recipe):
	""" tests if the needed drink for a recipe are plugged in. returns bool
	recipe: recipe name [str]
	"""
	global drinks

	file1 = open(dir_recipes + recipe, 'r')					# open file
	needed_drinks = file1.readlines()							# save lines as a list
	file1.close()

	needed_drinks.pop(0)			# remove info line

	for idx, i in enumerate(needed_drinks):						# loop thorugh every drink in list
		if needed_drinks[idx].endswith('\n'):						# remove trailing newline characters
			needed_drinks[idx] = needed_drinks[idx][:-1]

		c_idx = needed_drinks[idx].find(',')						# remove volume information
		needed_drinks[idx] = needed_drinks[idx][:c_idx]
	
	for d in needed_drinks:
		if not d in plugs:
			#print("DR TA d: " + str(d))
			return False												# return False, if drink d is not plugged in
	
	return True															# return True, as everything seems to be there


""" ### set drinks ### """
def set_drink(plug, drink):
	""" set drink
	plug: number of the plug (1-6) [int]
	drink: EITHER drink name or "None" for reset [string] OR index for drinks list (1-end of list, because 0 is cleaning_water) (-1: reset) [int]
	"""
	global drinks, plugs

	if plug < 1 or plug > 6:
		return					# break when wrong plug given

	if not (type(drink) == int or type(drink) == str or drink is None):		# break when input type not correct
		return

	if type(drink) == int:		# get drink name when index given
		drink = drinks[drink]
	
	if not (drink in drinks or drink is None):
		return					# break when drink is not available
	
	plugs[plug] = drink			# set drink on plug


""" ### GETTER METHODS ### """
""" used to get different lists"""
def get_drinks():
	return drinks

def get_plugs():
	return plugs

def get_recipes(available=None):
	""" returns recipes as a list
	available=None: filter recipes 
	[None: no filter, True: returns only available recipes, False: returns only unavailable recipes]
	"""
	global recipes

	return_list = []

	if available == None:
		return_list = recipes			# no filter applied, so everything will be returned
	elif available == True:
		for r in recipes:						# only adds the available recipes to the return list
			if _test_availability(r):
				return_list.append(r)
	elif available == False:
		for r in recipes:						# only add the unavailable recipes to the return list
			if not _test_availability(r):
				return_list.append(r)
	
	return return_list		# actually returns the list

def get_still_mixing():
	global is_mixing
	return is_mixing


""" ### ### MIXING METHODS ### ### """
def start_mixing(recipe):
	""" compiles the recipe and starts the mixing process.
	recipe: EITHER as string with recipe name OR as int with index in recipes list
	"""
	global is_mixing, recipe_step, commands, recipes

	if is_mixing:										# break, when there's already a recipe mixing
		return

	if type(recipe) != int and type(recipe) != str:		# break when input type not correct
		return

	if type(recipe) == int:								# get recipe name when index given
		recipe = recipes[recipe]
	
	if not _test_availability(recipe):					# break when recipe not available
		return
	
	file1 = open(dir_recipes + recipe, 'r')				# open file
	steps = file1.readlines()							# save steps as a list
	file1.close()

	steps.pop(0)			# remove info line

	for idx, i in enumerate(steps):
		if steps[idx].endswith('\n'):					# remove trailing newline characters
			steps[idx] = steps[idx][:-1]

	commands.clear() 									# delete previous commands
	""" compile recipe """
	for step in steps:								# compile step by step
		list = step.split(',')							# [<drink>, <volume>]
		time = int(list[1]) * gl.TIME_PER_ML			# calculate needed time
		plug = plugs.index(list[0])						# get the plug

		commands.append("o" + str(plug))				# open valve
		commands.append("t" + str(time))				# set timer
		commands.append("w")							# wait for timer to pass
		commands.append("c" + str(plug))				# close valve
	
	commands.append("e")					# end sign
	print("DR SM compiling done")
	print("DR commands:")
	for c in commands:
		print(c)
 
	# start the mixing process
	is_mixing = True
	recipe_step = 0	


def update_mixing():
	global is_mixing, recipe_step, commands, finishing_time

	if is_mixing:				# if a cocktail is currently mixed
		cmd = commands[recipe_step]
		if cmd[0] == 'o':					# open valve
			print("DR UM open valve " + str(cmd[1]))
			io.writeOutput(io.VALVES[int(cmd[1])], 1)
			io.writeOutput(io.PUMP, 1)
			recipe_step += 1

		elif cmd[0] == 'c':					# close valve
			print("DR UM close valve " + str(cmd[1]))
			io.writeOutput(io.VALVES[int(cmd[1])], 0)
			io.writeOutput(io.PUMP, 0)
			recipe_step += 1

		elif cmd[0] == 't':					# set timer
			print("DR UM set timer " + str(float(cmd[1:]) / 1000.0))
			finishing_time = time.time() + (float(cmd[1:]) / 1000.0)
			recipe_step += 1

		elif cmd[0] == 'w':					# wait
			t = time.time()
			if t >= finishing_time:				# if waited long enough, advance to next step
				recipe_step += 1
				
		elif cmd[0] == 'e':					# end sign
			print("DR UM end mixing")		# stops the mixing process
			is_mixing = False	
		

		# add debug information
		if gl.show_debug:
			gl.debug_text.append("MIX cur. cmd.: " + str(cmd) + "; prev. cmd.: " + str(commands[recipe_step-1]))
			gl.debug_text.append("MIX cmd nr.: " + str(recipe_step) + " / " + str(len(commands)))
