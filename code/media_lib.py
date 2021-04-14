"""
contains class for graphics, animations and videos
"""

import os						# used to scan for files and to execute commands from a commandline
#from sys import path			# random function to get random list index in video class
import pygame					# used in Animation-Class for displaying sprites
import pygame.freetype			# used in Button class to show text
import cv2 						# used in Video-Class for displaying videos
import numpy as np 				# used by opencv
import globals as gl			# imports global variables

class Image:
	""" can be used to easily display single images
	"""

	def __init__(self, path, x, y, width, height, rotation=0, show=True):
		""" create single sprites and easily display them
		- path:	complete path to the image file
		- x:	position on x-axis
		- y:	position on y-axis
		- width:	width of image (doesn't have to be as the original files, image can be stretched)
		- height:	height of image ( -- '' --)
		- rotation=0:	set a certain rotation to the image (optional)
		- show=True:	don't display image directly, when set to False
		"""
		self.img = pygame.transform.scale(pygame.image.load(path), (width, height))
		self.x, self.y = x, y
		if rotation != 0:
			self.img = pygame.transform.rotate(self.img, rotation)
		self.show = show

	def draw(self):
		if self.show:
			gl.screen.blit(self.img, (self.x, self.y))


class Button:
	""" class for drawing Buttons with different states """

	def __init__(self, path, img_normal, img_selected, img_disabled, x, y, width, height, direct_load=True, disabled=False, selected=False, rotation=0):
		""" draw single sprites 
		- path: complete path to folder with the files
		- img_normal, img_selected, img_disabled:
			file names for the images
		- x: x-position
		- y: y-position
		- width: width of image
		- height: height of image
		- direct_load=False: set True, when the image should directly be loaded
		- disabled=False: set directly on disabled
		- selected=False: set directly as selected
		"""
		path = path					# save paths
		self.path_normal 	= path + img_normal
		self.path_disabled 	= path + img_disabled
		self.path_selected 	= path + img_selected

		self.x, self.y = x, y						# save x and y coordinates
		self.width, self.height = width, height		# save width and height

		# settings
		self.show = False			# 'turn' image on and off
		self.disabled = disabled	# save if image is disabled (greyed out)
		self.selected = selected	# save if image is selected (somehow marked)
		self.rotation = rotation	# save rotation

		# pygame.Surface objects
		self.img_normal 	= None
		self.img_disabled 	= None
		self.img_selected 	= None

		# text params
		self.show_text = False
		self.text = ""
		self.font = None
		self.font_col = (0, 255, 0)
		self.hor_alignment = 0				# 0 = center, 1 = left, 2 = right
		self.ver_alignment = 0				# 0 = center, 1 = up, 2 = down

		if direct_load == True:
			self.load_image()
	
	def add_text(self, text, font, col, hor_alignment=0, ver_alignment=0):
		""" add text to button
		- text: text to show [String]
		- font: font
		- col: color to use (R, G, B)
		- hor_alignment=0: horicontal alignment (0 = center, 1 = left, 2 = right)
		- ver_alignment=0: vertical alignment (0 = center, 1 = up, 2 = down)
		"""
		self.show_text = True
		self.text = text
		self.font = font
		self.font_col = col
		self.hor_alignment = hor_alignment
		self.ver_alignment = ver_alignment
	
	def load_image(self):
		""" loads image as pygame.Surfaces """
		self.img_normal		= Image(self.path_normal	, self.x, self.y, self.width, self.height, self.rotation)
		self.img_disabled	= Image(self.path_disabled	, self.x, self.y, self.width, self.height, self.rotation)
		self.img_selected	= Image(self.path_selected	, self.x, self.y, self.width, self.height, self.rotation)
		self.show = True
	
	def unload_image(self):
		""" deletes pygame.Surface objects """
		self.img_normal 	= None
		self.img_disabled 	= None
		self.img_selected 	= None
		self.show = False
	
	def draw(self):
		"""
		draw the image
		"""

		if self.show:			# draw image based on settings
			if self.disabled:
				self.img_disabled.draw()
			else:
				if self.selected:
					self.img_selected.draw()
				else:
					self.img_normal.draw()
			
			if self.show_text:
				t_x, t_y = self.x, self.y
				textsur, rect = self.font.render(self.text, self.font_col)	# render text
				spacing = 15

				if self.hor_alignment == 0:				# position text based on hor_alignment, ver_alignment, button size and rectangle size of text
					t_x += self.width/2 - rect.width/2
				elif self.hor_alignment == 1:
					t_x += spacing
				elif self.hor_alignment == 2:
					t_x += self.width - rect.width - spacing

				if self.ver_alignment == 0:
					t_y += self.height/2 - rect.height/2
				elif self.ver_alignment == 1:
					t_y += spacing
				elif self.ver_alignment == 2:
					t_y += self.height - rect.height - spacing

				gl.screen.blit(textsur, (t_x, t_y))		# finally blit it


class Animation:
	"""
	this class handles the sprites/spritesheets folders and makes videos out of these.
	"""

	def __init__(self, folder_path):
		""" animation class. uses sprites do display a video
		- folder_path: complete path to media folder
		"""
		self.path = folder_path
		self.w, self.h = pygame.display.get_surface().get_size()
		# Images
		self.img_path = []								# save all paths to the image files
		for filename in os.listdir(self.path):
			if filename != "forwards.wav" and filename != "backwards.wav":
				self.img_path.append(self.path + filename)
		self.img_path.sort()		# make sure they are in the right order
		self.img = []				# will hold the pygame.Surface objects as soon they will be loaded
		self.n_frames = 0			# number of frames. is updated with every change on self.img[]
		# States / params
		self.loaded =  False		# frames loaded
		self.play = False			# video plays
		self.interrupt = False		# video is paused
		self.frame = 0				# durrent frame
		self.forwards = True		# video is played forwards
		self.repeat = False			# video plays on repeat

	def load(self):
		""" loads the frames as pygame.Surface. please use sparingly to keep RAM clear
		"""
		if not self.loaded:
			for i in self.img_path:
				self.img.append(pygame.transform.scale(pygame.image.load(i), (self.w, self.h)))
			self.n_frames = len(self.img)
			self.loaded = True
		

	def unload(self):
		""" unloads the n_frames. use it to clear up ram
		"""
		self.img.clear()
		self.n_frames = len(self.img)
		self.loaded = False

	def start(self, forwards=True, repeat=False):
		"""	start video from the beginning
		- forwards=True: set False, if you want play it backwards
		- repeat=False: set True, to endlessly repeat the video
			(can be stopped with stop())
		"""
		if self.loaded == False:		# interrupt when images are not loaded
			return

		self.play = True			# start video
		self. interrupt = False		# un-pause video, just in case
		self.forwards = forwards	# set params
		self.repeat = repeat
		
		if forwards:				# set start frame and start audio (when exiting and not muted)
			self.frame = 0
		else:
			self.frame = self.n_frames - 1

	def pause(self):
		""" interrupt / un-pause the video
		"""
		self.interrupt = not self.interrupt
	
	def stop(self):
		""" stop the video
		"""
		self.play = False

	def draw(self):
		""" draws the video
		"""
		if self.play:		# when video plays
			gl.screen.blit(self.img[self.frame], (0, 0))		# draw current frame
			
			if not self.interrupt:		# when not paused
				if self.forwards:		
					self.frame += 1								# advance frame
					if self.frame >= self.n_frames:				# if at the end
						if self.repeat:							# if repeat on
							self.frame = 0	
						else:
							self.play = False					# stop
				else:
					self.frame -= 1								# advance frame
					if self.frame < 0:							# if at the end
						if self.repeat:							# if repeat on
							self.frame = self.n_frames - 1		# start over
						else:
							self.play = False					# stop


class Video:
	""" 
	uses opencv to play videos
	"""

	def __init__(self, file):
		""" video class. uses opencv to display a video
		- file: complete path to the file
		"""
		self.file = file					# add the directory path to the file names

		self.cap = None									# holds the Video-Capture-object for playing the file
		
		# stats / params
		self.play = False
		self.repeat = False
		self.frames = 0
		self.frame_counter = 0
		self.audio_on = True

	def start(self, repeat=False):
		""" starts the video
		- repeat=False: set True, to play repeatedly
		"""
		self.play = True
		self.repeat = repeat
		self.cap = cv2.VideoCapture(self.file)
		self.frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
		self.frame_counter = 0

	def stop(self):
		""" stop the video
		"""
		self.play = False
	
	def draw(self):
		""" draw the video
		- screen: the pygame screen object
		"""
		if self.play:
			ret, frame = self.cap.read()
			self.frame_counter += 1

			if(self.test_for_last_frame()):
				if self.repeat:
					self.frame_counter = 0
					self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
				else:
					self.play = False
			
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			frame = frame.swapaxes(0, 1)
			pygame.surfarray.blit_array(gl.screen, frame)
	
	def test_for_last_frame(self):
		return self.frame_counter == self.frames


"""
The following two functions are used by the textfield class.
They are copied from the pygame wiki and slightly modified (this includes comments, one change to adapt it to freetype and the ability to do text breaks)
Source: http://www.pygame.org/wiki/TextWrapping?parent=CookBook
"""
def truncline(text, font, maxwidth):
	real=len(text)
	
	stext=text
	
	#l=font.size(text)[0]

	textsur, rect = font.render(text, (0,0,0))
	l = rect.width

	cut=0
	a=0                  
	done=1
	old = None
	while l > maxwidth:
		a=a+1
		n=text.rsplit(None, a)[0]
		if stext == n:
			cut += 1
			stext= n[:-cut]
		else:
			stext = n
		#l=font.size(stext)[0]

		textsur, rect = font.render(stext, (0,0,0))
		l=rect.width

		real=len(stext)               
		done=0                        
	return real, done, stext             
		
def wrapline(text, font, maxwidth): 
	""" this functions splits a string into a list, making lines that fit into a given width.
	It can also deal with newlines by first splitting the text into paragraphs (sort of), then applieing the the 
	text-break to each paragraph and putting this into a final list.
	"""


	all_lines = []			# includes all lines, with textbreak and newline chracters included

	ntext = text.split('\n')			# the text, but split into the lines ('n' as in newlin

	#print("[ML WL] split to newlines:", ntext)

	for line in ntext:					# then goes through the lines (or paragraphs if you will)
		done=0 
		wrapped=[]

		while not done:   				# in this while all the text break magic happens
			nl, done, stext=truncline(line, font, maxwidth) 
			wrapped.append(stext.strip())                  
			line=line[nl:]

		for wrapped_line in wrapped:			# puts all new wrapped lines to the list
			all_lines.append(wrapped_line)

	#print("[ML WL] all wrapped lines:", all_lines)                           
	return all_lines


class TextField:
	""" this class shows a textfield in a given space. 
	It allows different alignments (center, left, right) and automatic text wrapping
	"""

	x, y, width, height = 0, 0, 0, 0

	lines = []

	show_background = False
	background = None

	def __init__(self, x, y, width, height, text, font, font_col, alignment=1):
		""" creates text in agiven space
		- x:	x-Position
		- y:	y-position
		- width:	width of textfield
		- height:	height of textfield
		- text:	the text you want to display
		- font:	the to be used
		- font_col:	color in RGB-format as a tuple
		- alignment=1: horizontal alignment (0 = center, 1 = left, 2 = right)
		"""
		self.x, self.y = x, y							# save coordinates
		self.width, self.height = width, height			# save 
		self.alignment = alignment
		self.font = font
		self.font_color = font_col
		
		# create lines of text
		self.lines = wrapline(text, font, width)		# splitting the text in a list of words

	def change_text(self, text):
		self.lines = wrapline(text, self.font, self.width)

	def add_background(self, path):
		""" add a background image
		- path:	complete path to image file
		"""

		# the background is added as a Button object with only one image shown
		self.background = Image(path, self.x, self.y, self.width, self.height)
		self.show_background = True

	def draw(self):
		""" draw the textfield
		"""

		# if background is used
		if self.show_background:
			self.background.draw()
		
		spacing = 15			# space between lines and padding on the sides
		t_x, t_y = self.x, self.y + spacing		# set starting coordinates
		for text in self.lines:					# for each line
			
			textsur, rect = self.font.render(text, self.font_color)	# render text

			if self.alignment == 0:				# position text based on alignment, field size and rectangle size of text
				t_x += self.width/2 - rect.width/2
			elif self.alignment == 1:
				t_x += spacing
			elif self.alignment == 2:
				t_x += self.width - rect.width - spacing

			gl.screen.blit(textsur, (t_x, t_y))		# finally blit it

			t_y += rect.height + 5
			t_x = self.x


class Bar:

	def __init__(self, path, x, y, width, height, state=0, rotation=0):
		""" this class provides a bar (for example progress bar) with 11 states (0% - 100% in measures of 10%)
		path:	complete path to folder with the sprites (named in the correct order (i.e. a.png to k.png), starting at 0%)
		x:		x-coordinate of bar
		y:		y-coordinate of bar
		width:	width of bar
		height:	height of bar
		state=0:	the state of the bar (0-100, will be rounded to the next ten)
		rotation=0:	add a rotation to the bar (if needed; going clockwise)

		NOTE:the images need to be the same size as 100%, completely filling the area. If necessary, use the alpha channel.
		"""

		img_path = []								# save all paths to the image files
		for filename in os.listdir(path):
			img_path.append(path + filename)
		img_path.sort()								# sort it, just to be safe

		self.imgs = []								# creating the Image objects from the file paths
		for i in img_path:	
			self.imgs.append(Image(i, x, y, width, height, rotation, show=False))

		self.x, self.y = x, y						# saving paramters
		self.width, self.height = width, height

		self.state = 0								# saves the state / progress
		self.set_state(state)						# also, set the state

	def set_state(self, state):
		""" set the state of the bar to a new state. will be rounded to the next ten
		state:	set the new state (0-100)
		"""
		self.imgs[self.state].show = False		# disables the current image
		self.state = int(round(state/10))		# change to new image
		self.imgs[self.state].show = True		# enable the new current Image

	def draw(self):
		""" draw the bar """
		for i in self.imgs:
			i.draw()				# draws all images, though only one is enbabled and will be actually drawn



""" VLCVideo class deleted. Commit: 2a1128a723551cc48cc0ad81b7ee75fbd4958f82 """