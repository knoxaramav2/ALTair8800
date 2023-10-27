from tkinter import IntVar
from defs import *

class DisplayState:

    switches = {}
    leds = {}

    #Methods
    def toggle_led(self, led:Led):
        v = self.leds[led]
        v.set(1 - v.get())

    def toggle_switch(self, switch:Switch):
        v = self.switches[switch]
        v.set(1 - v.get())

    def shutoff_display(self):
        for n in self.leds:
            n.set(0)

    def __init__(self):
        for n in Switch:
            self.switches[n.name] = IntVar(value=0)

        for n in Led:
            self.leds[n.name] = IntVar(value=0)
