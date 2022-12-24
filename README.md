# circuitpython-cpxFireplace

This program is a simple LED fireplace running on an Adafruit Circuit Playground Express (CPX) board. A fireplace sound effect (looping `.wav` file) can be turned on and off using the CPX onboard slide switch.

## Explanation

There are two versions of pyFireplace:

`cpxFireplace_simple.py` is a perpetually burning fire.

`cpxFireplace_timer.py` allows you to set a sleep timer to automatically turn off the fire

The "fire" is created by randomly lighting one of the LEDs (a spark), then reducing the intensity of all of the LEDs by a small amount. New sparks continue to generate as all previous sparks fade away.

The sound is a looped .wav file (`fireplace.wav`).

## Installation

Copy the `fireplace.wav` file into a `resources/sound` directory on your board.

Copy one of the two pyFireplace python files and rename to `main.py` at the top level of your board.

When properly configured, your CIRCUITPY drive should contain:

```
/resources
	/sound
		fireplace.wav

main.py
```

## Sleep Timer Operation

With `cpxFireplace_timer.py`, by default, the fire is perpetual and will burn forever.

If you press either `A` or `B` button on the Circuit Playground Express it will enter sleep mode and show the current sleep time. Each LED represents 12 minutes for a total of two hours.

Continue to press `A` and `B` buttons to increase/decrease sleep time. When you're finished, the fire will resume on its own.

Anytime, even after the sleep timer expires, you can use the `A`/`B` buttons to  adjust the sleep time.

To return to perpetual burning, press the `reset`  button.
