

from enum import Enum
from tkinter import Button, Canvas, Checkbutton, Label, PhotoImage

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
        'btn_blue',
        'btn_red',

        'swt_black',
        'swt_blue',
        'swt_red',

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

    upper_text      :   str
    lower_text      :   str

    upper_lbl       :   Label
    lower_lbl       :   Label

    state           :   int
    imgs            :   [PhotoImage]

    base            : any = None
    var             : any = None
    type            : ctrl_type

    def __init__(self, cvc, x, y, 
                 lbl:str, img_fam:ctrl_clr, type:ctrl_type, comm=None) -> None:
        self.grid = cvc
        spl_str = lbl.split('|')
        ln = len(spl_str)
        self.upper_text = spl_str[0] if ln >= 1 else ''
        self.lower_text = spl_str[1] if ln >= 2 else ''
        self.imgs = get_imgs(img_fam)

        if type == ctrl_type.led:
            self.base = Checkbutton(
                cvc, #state='disabled',
                activebackground=CHROMA, selectcolor=CHROMA,
                selectimage=self.imgs[1],
                command=comm,
                variable=self.var, indicatoron=False
            )
        
        self.base.configure(image=self.imgs[0])
        self.base.configure(bd=0, borderwidth=0, width=BOX_SZ, height=BOX_SZ)
        self.base.configure(bg=CHROMA)
        self.base.grid(column=x, row=y, padx=5, pady=5, sticky='NSEW')

class CtrlLed(Ctrl):
    def __init__(self, cvc, x, y, lbl: str, img_fam:ctrl_clr) -> None:
        super().__init__(cvc, x, y, lbl, img_fam, ctrl_type.led)

class CtrlSwitch(Ctrl):
    def __init__(self, cvc, x, y, lbl: str, img_fam:ctrl_clr) -> None:
        super().__init__(cvc, x, y, lbl, img_fam, ctrl_type.led)