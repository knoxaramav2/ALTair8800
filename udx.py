#User Device Exchange

from state import SharedState

def reset_toggle(name):
        SharedState().toggle_switch(name)
        print(SharedState().switches[name].get())