

from enum import Enum
from tkinter import Label


sw_state = Enum(
    'SW_STATE', [
        'UMD', 'UD'
    ]
)

ctrl_clr = Enum(
    'CTRL_CLR', [
        'red', 
        'green',
        'blue',
        'black',
        'white'
    ]
)

class Ctrl:
    x       : int
    y       : int
    abspos  : bool #pixel placement if true

    def __init__(
            self, 
            x, 
            y, 
            abspos=False):
        self.x = x
        self.y = y
        self.abspos = abspos

class CtrlSwitch(Ctrl):
        
        label       : Label

        def __init_ud(self):
             pass

        def __init_umd(self):
             pass

        def __init__(
                  self,
                  x, 
                  y, 
                  abspos=False,
                  state:sw_state=sw_state.UMD,
                  clr:ctrl_clr=ctrl_clr.red,
                  comm:str=''
                  ):
            super().__init__(x, y, abspos)
            if state == sw_state.UMD:
                self.__init_umd()
            else:
                self.__init_ud()

class CtrlButton(Ctrl):
    def __init__(self, state:sw_state, clr:ctrl_clr) -> None:
        pass