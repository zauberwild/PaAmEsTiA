"""
contains class for graphics, animations and videos
"""

import os						# used to scan for files and to execute commands from a commandline
from random import randint		# random function to get random list index in video class
import pygame, pygame.mixer		# used in Animation-Class for displaying sprites and playing audio files
import pygame.freetype			# used in Button class to show text
import cv2 						# used in Video-Class for displaying videos
import numpy as np 				# used by opencv
import globals as gl

class Button:
	""" class for drawing Buttons with different states """

	def __init__(self, path, img_normal, img_selected, img_disabled, x, y, width, height, direct_load=True, disabled=False, selected=False):
		""" draw single sprites 
		- path: path to folder with the files
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
		path = gl.gen_path + path					# save paths
		self.path_normal 	= path + img_normal
		self.path_disabled 	= path + img_disabled
		self.path_selected 	= path + img_selected

		self.x, self.y = x, y						# save x and y coordinates
		self.width, self.height = width, height		# save width and height

		# settings
		self.show = False			# 'turn' image on and off
		self.disabled = disabled	# save if image is disabled (greyed out)
		self.selected = selected	# save if image is selected (somehow marked)

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
		- hor_alignment=0: hor_alignment (0 = center, 1 = left, 2 = right)
		- ver_alignment=0: hor_alignment (0 = center, 1 = up, 2 = down)
		"""
		self.show_text = True
		self.text = text
		self.font = font
		self.font_col = col
		self.hor_alignment = hor_alignment
		self.ver_alignment = ver_alignment
	
	def load_image(self):
		""" loads image as pygame.Surfaces """
		self.img_normal 	= pygame.transform.scale(pygame.image.load(self.path_normal), (self.width, self.height))
		self.img_disabled 	= pygame.transform.scale(pygame.image.load(self.path_disabled), (self.width, self.height))
		self.img_selected 	= pygame.transform.scale(pygame.image.load(self.path_selected), (self.width, self.height))
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
				gl.screen.blit(self.img_disabled, (self.x, self.y))
			else:
				if self.selected:
					gl.screen.blit(self.img_selected, (self.x, self.y))
				else:
					gl.screen.blit(self.img_normal, (self.x, self.y))
			
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
		- folder_path: path to media folder
		"""
		self.path = gl.gen_path + folder_path
		self.w, self.h = pygame.display.get_surface().get_size()
		# Images
		self.img_path = []								# save all paths to the image files
		for filename in os.listdir(self.path):
			if filename != "forwards.wav" and filename != "backwards.wav":
				self.img_path.append(self.path + filename)
		self.img_path.sort()		# make sure they are in the right order
		self.img = []				# will hold the pygame.Surface objects as soon they will be loaded
		self.n_frames = 0			# number of frames. is updated with every change on self.img[]
		# Audio
		self.audio_forwards_path = self.path + "forwards.wav"
		self.audio_backwards_path = self.path + "backwards.wav"
		self.audio_forwards = None		# holds pygame.mixer.Sound object,
		self.audio_backwards = None			# assuming correspoding audio files could be found
		if os.path.isfile(self.audio_forwards_path):		# test if audio files are there
			self.audio_forwards = pygame.mixer.Sound(self.audio_backwards_path)		# create object  with audio-file
		if os.path.isfile(self.audio_backwards_path):
			self.audio_backwards = pygame.mixer.Sound(self.audio_backwards_path)
		# States / params
		self.loaded =  False		# frames loaded
		self.play = False			# video plays
		self.interrupt = False		# video is paused
		self.frame = 0				# durrent frame
		self.forwards = True		# video is played forwards
		self.repeat = False			# video plays on repeat
		self.audio_mute = False		# video on mute

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

	def start(self,audio=True, forwards=True, repeat=False):
		"""	start video from the beginning
		- audio=True: set False to mute
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
		self.audio_mute = not audio
		
		if forwards:				# set start frame and start audio (when exiting and not muted)
			self.frame = 0
			if self.audio_forwards != None and audio:
				self._start_audio()
		else:
			self.frame = self.n_frames - 1
			if self.audio_backwards != None and audio:
				self._start_audio(forwards=False)
	
	def _start_audio(self, forwards=True):
		""" play the audio files (internal use only)
		- forwards=True: True: play forwards.wav / False: play backwards.wav
		"""
		if forwards:				# start audio (if exiting)
			if self.audio_forwards != None:
				pygame.mixer.Sound.play(self.audio_forwards)
		else:
			if self.audio_backwards != None:
				pygame.mixer.Sound.play(self.audio_backwards)

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
							if not self.audio_mute:				# start over
								self._start_audio()
							self.frame = 0	
						else:
							self.play = False					# stop
				else:
					self.frame -= 1								# advance frame
					if self.frame < 0:							# if at the end
						if self.repeat:							# if repeat on
							self.frame = self.n_frames - 1		# start over
							if not self.audio_mute:
								self._start_audio(forwards=False)
						else:
							self.play = False					# stop


class Video:
	""" 
	uses opencv to play videos
	"""

	def __init__(self, file, audio_file):
		""" video class. uses opencv to display a video
		- files: list of file paths. by pressing play, one will be chosen randomly
		"""
		self.file = gl.gen_path + file					# add the directory path to the file names
		self.audio_file = gl.gen_path + audio_file

		self.cap = None									# holds the Video-Capture-object for playing the file
		self.audio = None								# holds pygame.mixer.Sound object
		if os.path.isfile(self.audio_file):				# test if audio file is there
			self.audio = pygame.mixer.Sound(self.audio_file)	
		
		# stats / params
		self.play = False
		self.repeat = False
		self.frames = 0
		self.frame_counter = 0
		self.audio_on = True

	def start(self, repeat=False, audio=True):
		""" starts the video
		- repeat=False: set True, to play repeatedly
		- audio=True: True for audio, False for mute
		"""
		self.play = True
		self.repeat = repeat
		self.cap = cv2.VideoCapture(self.file)
		self.frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
		self.frame_counter = 0
		self.audio_on = audio
		if self.audio_on:				# if audio on
			self._start_audio()
	
	def _start_audio(self):
		""" plays the audio file"""
		pygame.mixer.Sound.play(self.audio)			# start audio

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
					if self.audio_on:
						self._start_audio()
				else:
					self.play = False
			
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			frame = frame.swapaxes(0, 1)
			pygame.surfarray.blit_array(gl.screen, frame)
	
	def test_for_last_frame(self):
		return self.frame_counter == self.frames


# global variables for video-class:
vlc_start_linux = "cvlc -f --no-video-title-show --play-and-exit --no-loop <path> &"			# command lines for vlc on various platforms
vlc_kill_linux = "killall vlc"																	# <path> will be replaced with a path
vlc_start_windows = "vlc --no-video-title-show --play-and-exit --no-loop <path>"
vlc_kill_windows = "TASKKILL /IM VLC.EXE"

class VLCVideo:
	"""
	this class can play videos with VLC Media Player by starting it from the command line
	"""

	def __init__(self, files, length):
		""" video class. starts vlc via commandline
		- files: list with all video files. if given multiple files, one will be chosen at random
		- length: according list with the length of the videos in seconds
		"""
		self.files = files
		self.length = length

		for i in range(len(self.files)):		# add the directory path to the file names
			self.files[i] = gl.gen_path + self.files[i]

		delete = []								# test if every file can be found
		for i in range(len(self.files)):
			if not os.path.isfile(self.files[i]):
				delete.append(i)
		delete.sort(reverse=True)				# sort the list to decreasing values, so the missing indexes won't affect other indexes that need to be deleted
		for i in delete:						# delete all files that couldn't be found
			del self.files[i]
			del self.length[i]
		
		# stats / params
		self.play = False
		self.chosen_file = 0
		self.t_start = 0
	
	def start(self):
		""" start the video
		"""
		commandline = ""		# prepare the commandline
		if gl.os_is_linux:
			commandline = vlc_start_linux
		else:
			commandline = vlc_start_windows
		self.chosen_file = randint(0,len(self.files)-1)		# choose a random file
		commandline = commandline.replace("<path>", str(self.files[self.chosen_file]))
		os.system(commandline)

	def kill(self):
		""" kill VLC process. might kill all running VLC-processes
		"""
		commandline = ""
		if gl.os_is_linux:
			commandline = vlc_kill_linux
		else:
			commandline = vlc_kill_windows
		os.system(commandline)