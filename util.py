
from ctypes import windll
import os
from tkinter import BooleanVar, Canvas


class Util:

    base_uri    : str
    rsc_uri     : str
    font_uri    : str

    def int_to_boolarr(self, val:int, arr:[BooleanVar]) -> None:
        val = int(val)
        for i in range(0, len(arr)):
            arr[i].set((val & 1 << i))

    def boolarr_to_int(self, arr:[BooleanVar]) -> int:
        ret = 0
        for i in range(len(arr)):
            ret |= arr[i].get() << i
        return int(ret)
    
    def set_trans(self, c:Canvas):
        hwnd = c.winfo_id()
        wnd_exstyle = windll.user32.GetWindowLongA(hwnd, -20)  # GWL_EXSTYLE
        new_exstyle = wnd_exstyle | 0x00080000  # WS_EX_LAYERED
        windll.user32.SetWindowLongA(hwnd, -20, new_exstyle)  # GWL_EXSTYLE
        windll.user32.SetLayeredWindowAttributes(hwnd, 0x008B0000, 255, 0x00000001)

    def __load_path(self):
        self.base_uri = os.path.dirname(__file__)
        self.rsc_uri = os.path.join(self.base_uri, 'rsc')
        self.font_uri = os.path.join(self.rsc_uri, 'fonts')

    def __init__(self) -> None:
        self.__load_path()
    
__inst__ : Util = None
def GetUtil():
    global __inst__
    if __inst__ is None:
        __inst__ = Util()
    return __inst__


