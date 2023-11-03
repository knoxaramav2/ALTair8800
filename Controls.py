

from enum import Enum
from tkinter import Button, Canvas, Checkbutton, Label

from defs import BOX_SZ, CHROMA
from rsc import GetRSC

#INPUTS
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

def create_fnc_list(self, fncs:str):
    fnc_list = fncs.split('|')
    for f in fnc_list:
        match f:
            case 'pop':
                pass
            case 'power':
                pass
            case _:
                pass

class Ctrl:
    grid            :   Canvas

    upper_text      :   str
    lower_text      :   str

    upper_lbl       :   Label
    lower_lbl       :   Label

    def __init__(self, cvc, lbl:str) -> None:
        self.grid = cvc
        spl_str = lbl.split('|')
        ln = len(spl_str)
        self.upper_text = spl_str[0] if ln >= 1 else ''
        self.lower_text = spl_str[1] if ln >= 2 else ''

class CtrlSwitch(Ctrl):

        def __get_imgs(self, clr:str):
            rsc = GetRSC()
            match clr:
                case ctrl_clr.black:
                    self.ctrl_up = rsc.input_photos['tgl_up_black']
                    self.ctrl_mid = rsc.input_photos['tgl_mid_black']
                    self.ctrl_down = rsc.input_photos['tgl_down_black']
                case ctrl_clr.red:
                    self.ctrl_up = rsc.input_photos['tgl_up_red']
                    self.ctrl_mid = rsc.input_photos['tgl_mid_red']
                    self.ctrl_down = rsc.input_photos['tgl_down_red']
                case ctrl_clr.blue:
                    self.ctrl_up = rsc.input_photos['tgl_up_blue']
                    self.ctrl_mid = rsc.input_photos['tgl_mid_blue']
                    self.ctrl_down = rsc.input_photos['tgl_down_blue']
                case _:
                    pass

        def __init__(
                  self, grid, clr, lbl
                  ):
            super().__init__(grid, lbl)
            self.__get_imgs(clr)

class CtrlSwitchUD(CtrlSwitch):
    
    def __init__(self, grid, x, y, clr, txt, comm):
        super().__init__(grid, clr, txt)
        ctrl = Checkbutton(
            grid, text="TEST TEXT",
            fg='white',
            border=0, bd=0, highlightthickness=0,
            activebackground=CHROMA, activeforeground=CHROMA,
            selectcolor=CHROMA, bg=CHROMA,
            indicatoron=False,
            selectimage=self.ctrl_up, image=self.ctrl_down,
            #width=BOX_SZ
        )
        ctrl.grid(column=x, row=y, padx=10, sticky='NSEW')

class CtrlSwitchUWD(CtrlSwitch):

    def __init__(self, grid, x, y, clr, txt, comm):
        super().__init__(grid, clr, txt)
        ctrl_u = Button(
            grid, text="TEST UWD",
            fg='white',
            border=0, bd=0, highlightthickness=0,
            activebackground=CHROMA, activeforeground=CHROMA,
            bg=CHROMA, image=self.ctrl_mid,
            #width=BOX_SZ
        )
        ctrl_u.grid(column=x, row=y, padx=10, sticky='NSEW')


class CtrlButton(Ctrl):
    def __init__(self, grid, x, y, clr, txt, comm):
        super().__init__(grid, txt)
        rsc = GetRSC()
        match clr:
            case ctrl_clr.blue:
                self.ctrl_up = rsc.input_photos['btn_up_blue']
                self.ctrl_down = rsc.input_photos['btn_down_blue']
            case _:
                pass

        ctrl = Button(
            grid, text='TEST BUTTON', fg='white',
            border=0, bd=0, highlightthickness=0,
            activebackground=CHROMA, activeforeground=CHROMA,
            bg=CHROMA, image=self.ctrl_up,
            #width=BOX_SZ
        )
        ctrl.grid(column=x, row=y, padx=10, sticky='NSEW')

#OUTPUTS
class Led(Ctrl):
    def __init__(self, grid, x, y, clr, lbl: str) -> None:
        super().__init__(grid, lbl)
        rsc=GetRSC()
        match clr:
            case ctrl_clr.green:
                self.ctrl_on = rsc.output_photos['led_on_green']
                self.ctrl_off = rsc.output_photos['led_off_green']
            case ctrl_clr.white:
                self.ctrl_on = rsc.output_photos['led_on_white']
                self.ctrl_off = rsc.output_photos['led_off_white']
            case ctrl_clr.red:
                self.ctrl_on = rsc.output_photos['led_on_red']
                self.ctrl_off = rsc.output_photos['led_off_red']
            case _:
                pass

        led = Checkbutton(
            grid, text='TEST BUTTON', fg='white',
                border=0, bd=0, highlightthickness=0,
                activebackground=CHROMA, activeforeground=CHROMA,
                state='disabled',
                bg=CHROMA, image=self.ctrl_off,
                indicatoron=False,
            #width=BOX_SZ
        )

        led.grid(column=x, row=y, padx=10, sticky='NSEW')