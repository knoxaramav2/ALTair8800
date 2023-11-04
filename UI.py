import tkinter as tk
from Controls import *
from Shared import SharedCPU, SharedMachine, SharedMem
from defs import *
from rsc import RSC, GetRSC
from util import GetUtil, Util
from tkinter import Button, Checkbutton, Radiobutton, Tk, Label, IntVar, BooleanVar, Canvas


class UI:

    #Shared Memory
    s_cpu       : SharedCPU
    s_mem       : SharedMem
    s_cmp       : SharedMachine

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

    def run(self):
        self.root.update()
        #TODO INIT LABELS
        self.root.mainloop()

    def __spacer(self, col, row, clr):
        Label(self.cvc, bd=0, borderwidth=0,
              #text='%s, %s'%(col, row), 
              #image=clr,
              fg='white',
              width=4, height=2,
              #width=BOX_SZ, height=BOX_SZ,
              highlightthickness=1, bg=CHROMA).grid(row=row, column=col, padx=5, pady=5)

    def __init_grid_dim(self):
        w = GetRSC().output_photos['led_off_white']
        for x in range(0,COLS):
            self.__spacer(x, 0, w)
        for y in range(0, ROWS):
            self.__spacer(0, y, w)

    def __init_inputs(self):
        c = self.cvc
        
        #ADDR
        sk = 0
        clr = ctrl_clr.swt_red
        offset = 5
        for i in range(0, 16):
            if i == 8: clr = ctrl_clr.swt_black
            pos = i+offset+sk
            CtrlSwitch(c, pos, ADDR_ROW_I, str(i), clr)
            if (i+3)%3 == 0: sk += 1
        
        CtrlSwitch(c, 2, CTRL_ROW, 'POWER', clr)

        offset = 5
        sk = 0
        ctrls = ['STOP|RUN', 'S. STEP', 'EXAMINE|EXAMINE NEXT',
                 'DEPOSIT|DEPOSIT NEXT', 'RESET|CLR', 'RESET|CLR', 
                 'PROTECT|UNPROTECT', 'AUX1', 'AUX2'
                 ]
        for i in range(0, len(ctrls)):
            pos = i + offset + sk
            if i == 1:
                CtrlButton(c, pos, CTRL_ROW, ctrls[i], ctrl_clr.btn_blue)
            elif i == 7 or i == 8:
                CtrlSwitch(c, pos, CTRL_ROW, ctrls[i], ctrl_clr.swt_blue)
            else:
                CtrlSwitch(c, pos, CTRL_ROW, ctrls[i], ctrl_clr.swt_blue, False)
            sk += 1

    def __init_outputs(self):
        c = self.cvc

        #ADDR
        sk = 0
        offset = 5
        for i in range(0, 16):
            pos = i+offset+sk
            CtrlLed(c, pos, ADDR_ROW_O, 'A%s'%i, ctrl_clr.led_red)
            if (i+3)%3 == 0: sk += 1

        #DATA
        sk = 0
        offset = 16
        for i in range(0, 8):
            pos = i+offset+sk
            CtrlLed(c, pos, STAT_ROW, 'A%s'%i, ctrl_clr.led_red)
            if (i+3)%3 == 1: sk += 1

        #STATUS
        offset = 2
        status = ['INTE', 'PROT', 'MEMR', 'INP', 'M1', 'OUT' 'HLTA', 'STACK', 'WO', 'INT']#Todo shared dictionary
        for i in range(len(status)):
            s = status[i]
            CtrlLed(c, i+offset, STAT_ROW, s, ctrl_clr.led_red)

        #HALT
        CtrlLed(c, 2, ADDR_ROW_O, 'WAIT', ctrl_clr.led_red)
        CtrlLed(c, 3, ADDR_ROW_O, 'SINGLE\nSTEP', ctrl_clr.led_red)

        CtrlLed(c, 2, ADDR_ROW_I, 'POWER', ctrl_clr.led_grn)

    def __init_ux(self):
        self.root = tk.Tk()
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

    def __init__(self, scpu, smem, scmp):
        self.util = GetUtil()

        #Shared        
        self.s_cpu = scpu
        self.s_mem = smem
        self.s_cmp = scmp

        #UI setup
        self.__init_ux()
        self.util.set_trans(self.cvc)

    
        

                


