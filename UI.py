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

    def run(self):
        self.root.update()
        #TODO INIT LABELS
        self.root.mainloop()

    def __spacer(self, col, row):
        Label(self.cvc, bd=0, borderwidth=0,
              highlightthickness=0, bg=CHROMA).grid(row=row, column=col, pady=5)

    def __init_grid_dim(self):
        #for i in range(0, 25) : self.__spacer(i, 0)
        #for i in range(0, 9)  : self.__spacer(0, i)
        for i in range(0, 25):
            for j in range(0, 9):
                self.__spacer(i, j)

    def __init_inputs(self):
        row_ctrl = 8
        row_addr = 6
        c = self.cvc
        self.inputs['power'] = CtrlSwitchUD(c, 2,row_ctrl, 
            ctrl_clr.black, 'OFF|ON', 'POP|POWER')
        self.inputs['runstop'] = CtrlSwitchUWD(c, 6, row_ctrl,
            ctrl_clr.black, 'STOP|RUN', 'STOP|RUN')
        self.inputs['runstop'] = CtrlButton(c, 8, row_ctrl,
            ctrl_clr.blue, 'STEP', 'STEP')

    def __init_outputs(self):
        c = self.cvc
        ra = 4
        rs = 1
        self.outputs['power'] = Led(
            c, 1, 8, ctrl_clr.green, 'POWER'
        )

    def __init_ux(self):
        self.root = tk.Tk()
        self.rsc = GetRSC()
        r = self.root
        r.title('Altair8800')
        #r.iconphoto('')
        r.geometry('%sx%s'%(WIN_X, WIN_Y))
        r.resizable(False, False)
        r.configure(background='grey')
        r.grid_columnconfigure(0, weight=1, pad=50)
        r.grid_rowconfigure(0, weight=1, pad=50)
        bgp = Label(r, image=self.rsc.board_img)
        bgp.place(x=0, y=0, width=WIN_X, height=WIN_Y)
        self.cvc = tk.Canvas(r, background=CHROMA,
                             width=WIN_X, height=WIN_Y,
                             bd=0, border=0, highlightthickness=0,
                             relief='ridge'
                             )
        self.cvc.grid(row=0, column=0, pady=10, sticky='NW')
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

    
        

                


