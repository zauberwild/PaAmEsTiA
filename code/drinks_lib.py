"""
contains the recipe-class and drink-class
"""

# imports
import globals as gl
import io_lib as io
import os
import time
from media_lib import prompt_file		# both used to import new files
from shutil import copyfile

""" ### PATHS ### """
dir_recipes = gl.gen_path + "/src/recipes/"					# path to the recipe-directory

""" ### STORAGE ### """
plugs = ["cleaning_water", "", "", "", "", ""]				# stores the drinks plugged in

drinks = []													# stores the available drinks to choose from

recipes = []												# stores all recipes that could be found in the recipe folder

""" variables for mixing """
is_mixing = False				# stores, if currently a recipe is mixing
recipe_step = 0					# stores the current step
commands = []					# compiled command lines
finishing_time = 0				# precalculated time, when the timer will be done

""" functions """
def current_milli_time():
	# returns the current unix-time in milliseconds
    return round(time.time() * 1000)


""" ### SETUP ### """
# this part will run once, as soon this file is imported somewhere

def update_recipes_and_drinks():
	global drinks, recipes
	drinks.clear()
	recipes.clear()

	# look for drinks
	file1 = open(gl.gen_path + "/src/drinks", 'r')			# open file
	drinks = file1.readlines()								# save lines as a list
	file1.close()
	file1 = open(gl.gen_path + "/src/drinks_custom", 'r')			# open file
	drinks += file1.readlines()								# save lines as a list
	file1.close()

	for idx, i in enumerate(drinks):						# remove trailing newline characters
			if drinks[idx].endswith('\n'):
				drinks[idx] = drinks[idx][:-1]
				
	print("[DR URD] drink list  content:")
	print(drinks)

	# look for recipes
	for filename in os.listdir(dir_recipes):
		recipes.append(filename)
	recipes.remove('free_mixed_recipe')				# sort the free mixed recipe, as it should not appear in the recipe list

	print("[DR URD] recipe list  content:")
	print(recipes)

	# sort lists
	if gl.os_is_linux:
		drinks.sort()
		recipes.sort()

update_recipes_and_drinks()

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

	if plug < 1 or plug > len(plugs)-1:
		return					# break when wrong plug given
		
	print("[DR SD] 1/4 valid plug given")

	if not (type(drink) == int or type(drink) == str or drink is None):		# break when input type not correct
		return
		
	print("[DR SD] 2/4 correct input type")

	if type(drink) == int:		# get drink name when index given
		drink = drinks[drink]
	
	print("[DR SD] 3/4 got drink name if necessarry")
	
	if not (drink in drinks or drink is None):
		return					# break when drink is not available
	
	print("[DR SD] 4/4 drink is available")
	
	plugs[plug] = drink			# set drink on plug


""" MANAGE RECIPES """
def add_drinks(new_drinks):
	""" add new drinks to the drink file
	drinks: a list of the new drinks
	returns True if successfull, False if an error occurred
	"""

	global drinks

	print("[DR AD] adding new drinks")

	file = open(gl.gen_path + "/src/drinks_custom", "a")
	for i in new_drinks:
		file.write(i+"\n")
	file.close()
	drinks.sort()

	print("[DR AD] finished adding new drinks")

	return True


def import_recipe():
	""" opens a file prompt to import a new recipe
	returns True if successfull, False if an error occurred
	"""
	file_path = prompt_file()			# select a file
	print("[DR IR] 1/ file path:", file_path)

	file = open(file_path, 'r')					# read the file and do a compatability check
	lines = file.readlines()
	file.close()
	for idx, i in enumerate(lines):						# remove trailing newline characters
		if lines[idx].endswith('\n'):
			lines[idx] = lines[idx][:-1]

	print("[DR IR] 2/ could read file and removed newline characters")

	new_drinks = []
	
	try:
		for i in lines[1:]:
			splitted = i.split(',')
			if not splitted[0] in drinks:
				new_drinks.append(splitted[0])
			amount = int(splitted[1])
	except ValueError:
		print("[DR IR] 3/ ValueError: couldn't convert to int")
		return(False)
	except IndexError:
		print("[DR IR] 3/ IndexError: couldn't split Commands into drink and amount needed")
		return(False)

	print("[DR IR] 3/ No faulty units")

	print("[DR IR] 4/ These new drinks will be added:", new_drinks)
	
	success = add_drinks(new_drinks)

	if success:
		print("[DR IR] 4/ New drinks added successfully")
	else:
		print("[DR IR] 4/ Error occured")

	print("[DR IR] 5/ copy drink to recipe folder")
	
	try:
		split = file_path.split('/')
		filename = split[-1]
		copyfile(file_path, gl.gen_path + "/src/recipes/" + filename)
	except Exception:
		print("[DR IR] an error occured while copying the file")
		return False

	update_recipes_and_drinks()
	print("[DR SI] 6/ update recipes and drinks")

	print("[DR SI] all done")

	return True

def delete_recipe(recipe):
	""" deletes recipe """
	print("[DR DelR]", "1/ starting deleting procedure")

	if type(recipe) != int and type(recipe) != str:		# break when input type not correct
		return

	print("[DR DelR]", "2/ correct input type")

	if type(recipe) == int:								# get recipe name when index given
		recipe = recipes[recipe]
	
	print("[DR DelR]", "3/ got recipe name from index (if needed)")

	if recipe in gl.immutable_recipes:
		print("[DR DelR] 4/ abort, recipe is immutable")
		return

	print("[DR DelR] 4/ recipe is allowed to be deleted")

	os.remove(gl.gen_path + "/src/recipes/" + recipe)

	print("[DR DelR] 5/ recipe successfully deleted")

	update_recipes_and_drinks()

	print("[DR DelR] 6/ updated recipes and drinks")
	print("[DR DelR] all done")

""" ### GETTER METHODS ### """
""" used to get different lists"""
def get_drinks():
	return drinks.copy()

def get_plugs():
	return plugs.copy()

def get_recipes(available=None):
	""" returns recipes as a list
	available=None: filter recipes 
	[None: no filter, True: returns only available recipes, False: returns only unavailable recipes]
	"""
	global recipes

	return_list = []

	if available == None:
		return_list = recipes.copy()			# no filter applied, so everything will be returned
	elif available == True:
		for r in recipes:						# only adds the available recipes to the return list
			if _test_availability(r):
				return_list.append(r)
	elif available == False:
		for r in recipes:						# only add the unavailable recipes to the return list
			if not _test_availability(r):
				return_list.append(r)
	
	return return_list.copy()		# actually returns the list

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
	
	print("[DR SM]", "1/4 no other recipe mixing")

	if type(recipe) != int and type(recipe) != str:		# break when input type not correct
		return

	print("[DR SM]", "2/4 correct input type")

	if type(recipe) == int:								# get recipe name when index given
		recipe = recipes[recipe]
	
	print("[DR SM]", "3/4 got recipe name from index (if needed)")
	
	if not _test_availability(recipe):					# break when recipe not available
		return
	
	print("[DR SM]", "4/4 recipe is available")
	print("[DR SM]", "all checks passed, compiling recipe")
	
	file1 = open(dir_recipes + recipe, 'r')				# open file
	steps = file1.readlines()							# save steps as a list
	file1.close()

	steps.pop(0)			# remove info line

	for idx, i in enumerate(steps):
		if steps[idx].endswith('\n'):					# remove trailing newline characters
			steps[idx] = steps[idx][:-1]

	commands.clear() 									# delete previous commands
	""" compile recipe """
	for step in steps:									# compile step by step
		list = step.split(',')							# [<drink>, <volume>]
		time = int(int(list[1]) * gl.TIME_PER_ML)		# calculate needed time	(in ms)
		plug = plugs.index(list[0])						# get the plug
		print("[DR SM]", "Plug:", plug,"corresponding drink:" , list[0])

		commands.append("o" + str(plug))				# open valve
		commands.append("t" + str(time))				# set timer
		commands.append("w")							# wait for timer to pass
		commands.append("c" + str(plug))				# close valve
	
	commands.append("e")					# end sign
	print("[DR SM] compiling done")
	print("[DR SM] commands:")
	for c in commands:
		print(c)
 
	# start the mixing process
	is_mixing = True
	recipe_step = 0	


def update_mixing():
	global is_mixing, recipe_step, commands, finishing_time

	if is_mixing:				# if something is currently mixed
		cmd = commands[recipe_step]
		if cmd[0] == 'o':					# open valve
			valve = int(cmd[1])
			print("[DR UM] open valve " + str(valve))
			io.writeOutput(io.VALVES[valve], 1)
			io.writeOutput(io.PUMP, 1)
			recipe_step += 1

		elif cmd[0] == 'c':					# close valve
			valve = int(cmd[1])
			print("[DR UM] close valve " + str(valve))
			io.writeOutput(io.VALVES[valve], 0)
			io.writeOutput(io.PUMP, 0)
			recipe_step += 1

		elif cmd[0] == 't':					# set timer
			print("[DR UM] set timer " + cmd[1:] + " ms")
			finishing_time = current_milli_time() + int(cmd[1:])
			recipe_step += 1

		elif cmd[0] == 'w':					# wait
			t = current_milli_time()
			if t >= finishing_time:				# if waited long enough, advance to next step
				recipe_step += 1
				
		elif cmd[0] == 'e':					# end sign
			print("[DR UM] end mixing")		# stops the mixing process
			is_mixing = False	
		

		# add debug information
		if gl.show_debug:
			gl.debug_text.append("MIX cur. cmd.: " + str(cmd) + "; prev. cmd.: " + str(commands[recipe_step-1]))
			gl.debug_text.append("MIX cmd nr.: " + str(recipe_step) + " / " + str(len(commands)))
