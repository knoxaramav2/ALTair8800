

from enum import Enum
from tkinter import BooleanVar, Button, Canvas, Checkbutton, Frame, IntVar, Label, PhotoImage, Radiobutton, Variable, Widget

from defs import BOX_SZ, CHROMA, IMG_SZ
from rsc import GetRSC

#INPUTS
sw_state = Enum(
    'SW_STATE', [
        'UMD', 'UD'
    ]
)

ctrl_clr = Enum(
    'CTRL_CLR', [
        'btn_blue',
        'btn_red',

        'swt_black',
        'swt_blue',
        'swt_red',
        'swt_white',

        'led_grn',
        'led_red',
        'led_wht',
    ]
)

ctrl_type = Enum(
    'ctrl_type',[
        'btn', 'sw2', 'sw3', 'led'
    ]
)

def get_imgs(img_fam:str):
    cols = []
    rsc = GetRSC()
    match img_fam:
        case ctrl_clr.btn_blue:
            cols.append(rsc.input_photos['btn_down_blue'])
            cols.append(rsc.input_photos['btn_up_blue'])
        case ctrl_clr.btn_red:
            cols.append(rsc.input_photos['btn_down_red'])
            cols.append(rsc.input_photos['btn_up_red'])

        case ctrl_clr.swt_black:
            cols.append(rsc.input_photos['tgl_down_black'])
            cols.append(rsc.input_photos['tgl_mid_black'])
            cols.append(rsc.input_photos['tgl_up_black'])
        case ctrl_clr.swt_blue:
            cols.append(rsc.input_photos['tgl_down_blue'])
            cols.append(rsc.input_photos['tgl_mid_blue'])
            cols.append(rsc.input_photos['tgl_up_blue'])
        case ctrl_clr.swt_red:
            cols.append(rsc.input_photos['tgl_down_red'])
            cols.append(rsc.input_photos['tgl_mid_red'])
            cols.append(rsc.input_photos['tgl_up_red'])
        case ctrl_clr.swt_white:
            cols.append(rsc.input_photos['tgl_down_white'])
            cols.append(rsc.input_photos['tgl_mid_white'])
            cols.append(rsc.input_photos['tgl_up_white'])
        case ctrl_clr.led_grn:
            cols.append(rsc.output_photos['led_off_green'])
            cols.append(rsc.output_photos['led_on_green'])
        case ctrl_clr.led_red:
            cols.append(rsc.output_photos['led_off_red'])
            cols.append(rsc.output_photos['led_on_red'])
        case ctrl_clr.led_wht:
            cols.append(rsc.output_photos['led_off_white'])
            cols.append(rsc.output_photos['led_on_white'])
        case _:
            pass
    return cols

def create_fnc_list(fncs:str):
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

    upper_text      :   str = ''
    lower_text      :   str = ''

    upper_lbl       :   Label
    lower_lbl       :   Label

    state           :   IntVar
    imgs            :   [PhotoImage]

    base            : Widget
    var             : Variable = None
    type            : ctrl_type

    def __init__(self, cvc, x, y, 
                 lbl:str, img_fam:ctrl_clr, type:ctrl_type, var:Variable=None):
        self.state = IntVar(cvc.master, value=0)
        self.var = var
        self.grid = cvc
        self.type = type
        spl_str = lbl.split('|')
        ln = len(spl_str)
        self.upper_text = spl_str[0] if ln >= 1 else ''
        self.lower_text = spl_str[1] if ln >= 2 else ''
        self.imgs = get_imgs(img_fam)
        if type == ctrl_type.led:
            self.base = Checkbutton(
                cvc, state='disabled',
                activebackground=CHROMA, selectcolor=CHROMA,
                background=CHROMA,#Needs to be here too for some reason
                selectimage=self.imgs[1],
                image=self.imgs[0],
                variable=self.var,
                indicatoron=False
            )

        elif type == ctrl_type.sw2:
            self.base = Checkbutton(
                cvc,
                activebackground=CHROMA, selectcolor=CHROMA,
                selectimage=self.imgs[2],
                image=self.imgs[0],
                variable=self.var, indicatoron=False
        )
        elif type == ctrl_type.sw3:
            self.base = Button(
                cvc, image=self.imgs[1],
                activebackground=CHROMA,
                highlightthickness=1
            )
        elif type == ctrl_type.btn:
            self.base = Button(
                cvc, image=self.imgs[1],
                activebackground=CHROMA,
            )
        self.base.configure(bd=0, borderwidth=0, background=CHROMA, width=BOX_SZ, height=BOX_SZ)
        self.base.configure(bg=CHROMA)
        self.base.grid(column=x, row=y, padx=5, pady=5, sticky='NSEW')

    def set_command(self, comm):
        self.base.configure(command=comm)
        return self

class CtrlLed(Ctrl):
    def __init__(self, cvc, x, y, lbl: str, img_fam:ctrl_clr, var:any=None):
        super().__init__(cvc, x, y, lbl, img_fam, ctrl_type.led, var)

class CtrlSwitch(Ctrl):
    def __init__(self, cvc, x, y, lbl: str, img_fam:ctrl_clr, twopoint=True, var:any=None):
        type = ctrl_type.sw2 if twopoint else ctrl_type.sw3
        super().__init__(cvc, x, y, lbl, img_fam, type, var)

class CtrlButton(Ctrl):
    def __init__(self, cvc, x, y, lbl: str, img_fam:ctrl_clr, var:any=None):
        super().__init__(cvc, x, y, lbl, img_fam, ctrl_type.btn, var)
