###################################################
# CircuitPython - Circuit Playground Express
#
# cpxFireplace
# Simulating a fire burning
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

import time
import board
import random
import neopixel
import audiocore
import digitalio
from audioio import AudioOut

YELLOW = (255, 150, 0)
def scale (a, b):
	return tuple(map((lambda x:max(min(round(x*b),255),0)),a))

# Set up pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.7, auto_write=False)

# Set up fire sound
fire_sound = audiocore.WaveFile(open("/resources/sound/fireplace.wav", "rb"))
audio = AudioOut(board.SPEAKER)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.switch_to_output(value=True)

# The Switch
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.switch_to_input(pull=digitalio.Pull.UP)

# Define the colors and starting intensities for 10 "flames"
flames = [YELLOW for i in range(10)]
intensity = [random.randint(5,255) for i in range(10)]

# Flames Eternal
playing = False
while True:
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
		pixels[i] = scale(flames[i], intensity[i]/255)
	pixels.show()
	time.sleep(.02)
