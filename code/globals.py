"""
this file stores all global variables and constants
"""

""" imports """
from pathlib import Path								# used to get the complete path of the working directory
from os import path											# used to get the complete path of the working directory
import pygame
import pygame.freetype

""" file paths """
gen_path = str(Path(__file__).parent.absolute())		# get the complete path of the "code"-directory

drink_file_path = gen_path + "/src/drinks"				# path of drinks file

""" output variables """
_UNIT_SIZE = 250 									# size of one unit in ml
_TIME_PER_UNIT = 25000								# time needed to fill one unit in milliseconds
TIME_PER_ML = _TIME_PER_UNIT / _UNIT_SIZE			# time pro milliliter in millisecond
GLASS_SIZE = 300									# size of the glass
CLEANING_TIME = 2000								# time for cleaning water to clean pipes (in milliseconds)

""" debug variables """
os_is_linux = not path.isfile(gen_path + "/src/.windows")		# looks for a ".windows" file, which only exists on my Windows-PC

show_debug = False		# show debugging information (fps,...)
debug_text = []			# debug list with all parameters to show. append parameters to this list every loop

pygame.freetype.init()
debug_font = pygame.freetype.Font(gen_path + "/src/fonts/CamingoCode-Regular.ttf", 24)		# debug font
debug_font_big = pygame.freetype.Font(gen_path + "/src/fonts/CamingoCode-Regular.ttf", 48)		# debug font, but bigger
debug_font_small = pygame.freetype.Font(gen_path + "/src/fonts/CamingoCode-Regular.ttf", 18)		# debug font, but smaller

standard_font_size = 18
standard_font = pygame.freetype.Font(gen_path + "/src/fonts/da_mad_rave/Da Mad Rave.otf", standard_font_size)

standard_font_size_small = 12
standard_font_small = pygame.freetype.Font(gen_path + "/src/fonts/da_mad_rave/Da Mad Rave.otf", standard_font_size_small)

""" setting window up """
prog_active = True		# set to False to end program

FPS = 24				# frames per second
W, H = 800, 600			# width and height of the window

prog_pos = 'i'			# saves current position in program flow
cr_prev_pos = ''		# this stores the previous position for the credits

screen = None
if os_is_linux:
	screen = pygame.display.set_mode((W,H), pygame.FULLSCREEN)		# create the window
	pygame.mouse.set_visible(False)			# hide cursor
else:
	screen = pygame.display.set_mode((W,H))

pygame.display.set_caption("paamestia_main")
clock = pygame.time.Clock()

""" immutable recipes """
immutable_recipes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Pangalaktischer Donnergurgler']

""" dictionary for recipes with their own video (path from /src/)"""
recipe_video_dict = {"2":"/src/media/intro/intro2.mp4",
					 "3":"/src/media/intro/intro3.mp4",
					 "4":"/src/media/intro/intro4.mp4",
					 }
""" notification """
notifications = []


""" credits """
credits_text = """PAAMESTIA

gebaut von André Milling, Max Schiemann, Dominic Kosin und Arvid Randow

GitHub-Repository: www.github.com/zauberwild/paamestia
veröffentlicht unter der MIT-Lizenz
"""
