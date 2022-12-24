###################################################
# CircuitPython - Circuit Playground Express
#
# cpxFireplace with sleep timer
#
# Simulating a fire burning
# Application begins in perpetal burning mode
# A/B buttons edit sleep time
# Slide-switch turns sound on/off
#
# MIT License
# 
# Copyright (c) 2022 Robert Gallup
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 

import math
import time
import board
import random
import neopixel
import audiocore
import digitalio
from audioio import AudioOut

# Colors
FIRE_COLOR = (255, 150, 0)
SLEEP_EDIT_COLOR = (0, 0, 100)
BRIGHTNESS = .5

# Each LED represents 12 minutes time for a total of 2 hours
sleep_increment = 12 * 60 # 12 minutes x 60 seconds
sleep_max       = 10 * sleep_increment
sleep_duration  =  1 * sleep_increment

# Parameters for button interaction to set fire timer (seconds)
key_repeat_time     =  .4
interaction_timeout = 3

# Utility: Multiply elements of a tuple (a) by a factor (b)
def mult(a, b):
	return tuple(map((lambda x:max(min(round(x*b),255),0)),a))

# Initialize pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=BRIGHTNESS, auto_write=False)

# Initialize fire sound
fire_sound = audiocore.WaveFile(open("/resources/sound/fireplace.wav", "rb"))
audio = AudioOut(board.SPEAKER)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.switch_to_output(value=True)

# Initialize the switch
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.switch_to_input(pull=digitalio.Pull.UP)

# Initialize the buttons
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

# Timer class (duration is in fractional seconds)
class timer(object):

	def __init__(self, duration):
		self.set(duration)
		self._running = False
		self._start_time = 0

	def set (self, duration):
		self._duration = duration
	
	reset = set

	def expired(self):
		if not self._running:
			return True
		else:
			is_expired = (time.monotonic()-self._start_time) >= self._duration
			self._running = not is_expired
			return is_expired

	def start(self):
		self._start_time = time.monotonic()
		self._running = True

	restart = start

	def resume(self):
		self._start_time += (time.monotonic() - self._time_stopped)
		self._running = True

	def stop(self):
		self._running = False
		self._time_stopped = time.monotonic()

	def remaining(self):
		return self._duration if not self._running else max(0, self._start_time + self._duration - time.monotonic())

sleep_timer = timer(sleep_duration)
interaction_timer = timer(interaction_timeout)

# Fade flame
def fade_fire():
	global pixels, FIRE_COLOR, fire_on

	color = FIRE_COLOR
	for l in range(10):
		color = mult(color, .6)
		for p in range(10):
			pixels[p] = color 
		pixels.show()
		time.sleep(.03)
	fire_on = False

# Display the current time remaining on the timer
def show_sleep_time(c):
	remaining_time = sleep_timer.remaining()
	for p in range(10):
		pixels[p] = 0 if ((9-p) * sleep_increment) >= remaining_time else c
	pixels.show()

# Diaplay and adjust sleep timer with buttons A/B
def sleep_adjust():
	global sleep_duration, sleep, fire_on
	
	sleep = True
	sleep_timer.stop()
	sleep_duration = sleep_timer.remaining()
	show_sleep_time(SLEEP_EDIT_COLOR)
	time.sleep(key_repeat_time)

	interaction_timer.start()
	while not interaction_timer.expired():

		if not (button_A.value or button_B.value):
			continue
		
		# One button or the other has been pressed
		if button_A.value:
			sleep_duration = min(sleep_max, sleep_duration + sleep_increment)
		else:
			sleep_duration = max(0,         sleep_duration - sleep_increment)

		sleep_timer.set (math.ceil(sleep_duration/sleep_increment)*sleep_increment)
		show_sleep_time(SLEEP_EDIT_COLOR)
		time.sleep(key_repeat_time)
		interaction_timer.restart()
		fire_on = True

	sleep_timer.start()

# Define the colors and starting intensities for 10 "flames"
flames = [FIRE_COLOR for i in range(10)]
intensity = [random.randint(5,255) for i in range(10)]

# Flames Eternal
playing = False
sleep = False
timer_value = 10
fire_on = True

while True:

	# If either button is pressed, view and adjust the timer
	if button_A.value or button_B.value:
		sleep_adjust()
	
	# If in sleep mode (rather than perpetual), if the timer is expired
	# close the fire down
	if sleep and sleep_timer.expired():
		if fire_on:
			fade_fire()
			audio.stop()
			playing = False
			sleep_timer.set(0)
		continue

	# Turn sound on/off with switch setting
	if switch.value and not playing:
		audio.play(fire_sound, loop=True)
		playing = True
	elif not switch.value and playing:
		audio.stop()
		playing = False

	for i in range(10):
		intensity[i] -= 4
		if intensity[i] <= 0:
			intensity[i] = random.randint(100,255)
		pixels[i] = mult(flames[i], intensity[i]/255)
	pixels.show()
	time.sleep(.02)
