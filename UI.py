from functools import partial
import tkinter as tk
from Controls import *
from Shared import SharedCPU, SharedCU, SharedMachine, SharedMem
from control_fncs import *
from defs import *
from rsc import RSC, GetRSC
from tk_manager import GetTK
from util import GetUtil, Util
from tkinter import Button, Checkbutton, Radiobutton, Tk, Label, IntVar, BooleanVar, Canvas, filedialog as fd


class UI:

    #Shared Memory
    s_cpu       : SharedCPU
    s_mem       : SharedMem
    s_cmp       : SharedMachine
    s_cu        : SharedCU

    util        : Util
    rsc         : RSC

    #Control and LEDs
    inputs      : dict = {}
    outputs     : dict = {}

    #UI components
    root        : Tk
    cvc         : Canvas
    chroma      : str

    #Misc
    rsc         : RSC
    util        : Util

    inputs      : dict = {}
    outputs     : dict = {}

    def run(self):
        self.root.update()
        self.__init_labels()
        self.util.set_trans(self.cvc)
        self.root.update()
        self.root.mainloop()

    def file_dialog(self, s_dir:str):
        ret = fd.askopenfilename(initialdir=s_dir)

        return ret

    def __create_label(self, ctrl:Ctrl, adj_y=0):
        x = ctrl.base.winfo_x()
        y = ctrl.base.winfo_y()
        w = ctrl.imgs[0].width()#Used as referebce
        ux = x+((w-(len(ctrl.upper_text)*CHAR_PX))/2)
        uy = y+adj_y
        lx = x+((w-(len(ctrl.lower_text)*CHAR_PX))/2)
        ly = y+50+adj_y
        
        ctrl.upper_lbl = Label(self.cvc, text=ctrl.upper_text,
            highlightthickness=0, bd=0, border=0,
            wraplength=200,
            bg=CHROMA, 
            font=(self.rsc.lbl_font, FONT_SZ),
            fg='white')
        ctrl.upper_lbl.place(x=ux, y=uy)
    
        ctrl.lower_lbl = Label(self.cvc, text=ctrl.lower_text,
            highlightthickness=0, bd=0, border=0,
            wraplength=200,
            bg=CHROMA,
            font=(self.rsc.lbl_font, FONT_SZ),
            fg='white')
        ctrl.lower_lbl.place(x=lx, y=ly)

    def __init_labels(self):
        for k, v in self.outputs.items():
            self.__create_label(v, -20)
        for k, v in self.inputs.items():
            self.__create_label(v, -20)

    def __spacer(self, col, row):
        Label(self.cvc, bd=0, borderwidth=0,
              fg='white',
              width=4, height=2,
              highlightthickness=0, bg=CHROMA).grid(row=row, column=col, padx=5, pady=5)

    def __init_grid_dim(self):
        for x in range(0,COLS):
            self.__spacer(x, 0)
        for y in range(0, ROWS):
            self.__spacer(0, y)

    def __init_inputs(self):
        c = self.cvc
        
        #ADDR
        sk = 0
        clr = ctrl_clr.swt_red
        offset = 5
        ni=15
        for i in range(0, 16):
            if i == 8: clr = ctrl_clr.swt_white
            pos = i+offset+sk
            sw2 = CtrlSwitch(c, pos, ADDR_ROW_I, str(ni), clr, var=self.s_cmp.addr_sw[ni])
            sw2.set_command(partial(toggle_addr, sw2))
            self.inputs['ADDR_%s'%ni] = sw2
            if (i+3)%3 == 0: sk += 1
            ni -= 1
        
        sw2 = CtrlSwitch(c, 2, CTRL_ROW, 'ON|OFF', clr, var=self.s_cmp.power_on)
        sw2.set_command(partial(toggle_power, sw2, self.s_cmp))
        self.inputs['POWER'] = sw2

        offset = 5
        sk = 0
        ctrls = ['STOP|RUN', 'S. STEP', 'EXAMINE|EXAMINE NEXT',
                 'DEPOSIT|DEPOSIT NEXT', 'RESET|CLR', 
                 'PROTECT|UNPROTECT', 'AUX1', 'AUX2'
                 ]
        for i in range(0, len(ctrls)):
            pos = i + offset + sk
            txt = ctrls[i]
            inp = None
            fnc = None

            match i:
                case 0:
                    inp = CtrlSwitch(c, pos, CTRL_ROW, txt, ctrl_clr.swt_blue, False, var=self.s_cu.wait)
                    fnc = partial(toggle_ctrl, inp, partial(stop_run, self, inp))
                case 1:
                    inp = CtrlButton(c, pos, CTRL_ROW, txt, ctrl_clr.btn_blue)
                    fnc = partial(click_ctrl, inp, partial(next_step, self, inp))
                case 2:
                    inp = CtrlSwitch(c, pos, CTRL_ROW, txt, ctrl_clr.swt_blue, False)
                    fnc = partial(toggle_ctrl, inp, partial(examine, self, inp))
                case 3:
                    inp = CtrlSwitch(c, pos, CTRL_ROW, txt, ctrl_clr.swt_blue, False)
                    fnc = partial(toggle_ctrl, inp, partial(deposit, self, inp))
                case 4:
                    inp = CtrlSwitch(c, pos, CTRL_ROW, txt, ctrl_clr.swt_blue, False)
                    fnc = partial(toggle_ctrl, inp, partial(reset, self, inp))
                case 5:
                    inp = CtrlSwitch(c, pos, CTRL_ROW, txt, ctrl_clr.swt_blue, False)
                    fnc = partial(toggle_ctrl, inp, partial(protect, self, inp))
                case 6:
                    inp = CtrlSwitch(c, pos+2, CTRL_ROW, txt, ctrl_clr.swt_black)
                case 7:
                    inp = CtrlSwitch(c, pos+2, CTRL_ROW, txt, ctrl_clr.swt_black)

            inp.set_command(fnc)
            self.inputs[txt] = inp
            sk += 1

    def __init_outputs(self):
        c = self.cvc

        #ADDR
        sk = 0
        offset = 5
        ni = 15
        for i in range(0, 16):
            pos = i+offset+sk
            led = CtrlLed(c, pos, ADDR_ROW_O, 'A%s'%ni, ctrl_clr.led_red, var=self.s_cmp.addr_buffer[ni])
            self.outputs['ADDR_%s'%ni] = led
            if (i+3)%3 == 0: sk += 1
            ni -= 1

        #DATA
        sk = 0
        offset = 16
        ni = 7
        for i in range(0, 8):
            pos = i+offset+sk
            self.outputs['DATA_%s'%ni] = CtrlLed(c, pos, STAT_ROW, 'D%s'%ni, ctrl_clr.led_red, self.s_mem.curr_data[ni])
            if (i+3)%3 == 1: sk += 1
            ni -= 1

        #STATUS
        offset = 2
        status = ['INTE', 'PROT', 'MEMR', 'INP', 'M1', 'OUT', 'HLTA', 'STACK', 'WO', 'INT']#Todo shared dictionary
        for i in range(len(status)):
            s = status[i]
            v = None
            match s:
                case 'INTE': v = self.s_cpu.inte
                case 'PROT': v = self.s_mem.protect
                case 'MEMR': v = self.s_cpu.memr
                case 'INP': v = self.s_cpu.inp
                case 'M1': v = self.s_cu.M1
                case 'OUT': v = self.s_cpu.out
                case 'HLTA': v = self.s_cpu.hlta
                case 'STACK': v = self.s_cpu.stack
                case 'WO': v = self.s_cpu.wo
                case 'INT': v = self.s_cpu.intt
                case _: pass

            self.outputs[s] = CtrlLed(c, i+offset, STAT_ROW, s, ctrl_clr.led_red, var=v)

        #HALT
        self.outputs['WAIT'] = CtrlLed(c, 2, ADDR_ROW_O, 'WAIT', ctrl_clr.led_red, var=self.s_cu.wait)
        self.outputs['HLDA'] = CtrlLed(c, 3, ADDR_ROW_O, 'HLDA', ctrl_clr.led_red, var=self.s_cpu.hlta)
        self.outputs['POWER'] = CtrlLed(c, 2, ADDR_ROW_I, 'POWER', ctrl_clr.led_grn, var=self.s_cmp.power_on)

    def __init_ux(self):
        self.root = GetTK()
        self.rsc = GetRSC()
        r = self.root
        r.title('Altair8800')
        #r.iconphoto('')
        r.geometry('%sx%s'%(WIN_X, WIN_Y))
        r.resizable(False, False)
        r.configure(background='grey')
        #r.grid_columnconfigure(0, weight=1, pad=50)
        #r.grid_rowconfigure(0, weight=1, pad=15500)
        bgp = Label(r, image=self.rsc.board_img)
        bgp.place(x=0, y=0, width=WIN_X, height=WIN_Y)
        self.cvc = tk.Canvas(r, background=CHROMA,
                             width=WIN_X, height=WIN_Y,
                             bd=0, border=0, highlightthickness=0,
                             relief='ridge'
                             )
        self.cvc.grid(sticky='NW')

        self.rsc  = GetRSC()

        self.__init_grid_dim()
        self.__init_inputs()
        self.__init_outputs()

    def __init__(self, scmp:SharedMachine):
        self.util = GetUtil()

        #Shared        
        self.s_cmp = scmp
        self.s_cpu = scmp.get_cpu()
        self.s_mem = scmp.get_mem()
        self.s_cu = scmp.get_cu()

        #UI setup
        self.__init_ux()

    
        

                


