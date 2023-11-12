from Shared import SharedMachine
from UI import UI
from dev import load_program
from tk_manager import GetTK


def init_hotkeys(cmp:SharedMachine, ui:UI):
    tk = GetTK()

    tk.bind('<F5>', lambda event: load_program(cmp, ui))
    