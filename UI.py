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

    def __spacer(self, col, row, clr):
        Label(self.cvc, bd=0, borderwidth=0,
              #text='%s, %s'%(col, row), 
              image=clr,
              fg='white',
              width=BOX_SZ, height=BOX_SZ,
              highlightthickness=0, bg=CHROMA).grid(row=row, column=col, padx=5, pady=5)

    def __init_grid_dim(self):
        g = GetRSC().output_photos['led_on_green']
        r = GetRSC().output_photos['led_on_red']
        w = GetRSC().output_photos['led_off_white']
        tk = GetRSC().input_photos['tgl_up_black']
        tb = GetRSC().input_photos['tgl_up_blue']
        tr = GetRSC().input_photos['tgl_up_red']
        for x in range(0,COLS):
            #self.__spacer(x, 0)
            for y in range(0, ROWS):
                self.__spacer(x, y, w)

        #ADDR
        sk = 0
        clr = g
        offset = 7
        for i in range(0, 16):
            if i == 8: clr = r
            pos = i+offset+sk
            print('%s, '%i, end='')
            self.__spacer(pos, ADDR_ROW_O, clr)
            if (i+3)%3 == 0: 
                sk += 1
                print()

        #DATA
        sk = 0
        offset = 18
        for i in range(0, 8):
            pos = i+offset+sk
            self.__spacer(pos, STAT_ROW, r)
            if i%3 == 1: sk += 1

        #STATUS
        offset = 3
        sk=0
        for i in range(0, 8):
            pos = i+offset+sk
            self.__spacer(pos, STAT_ROW, r)

        #HALT
        self.__spacer(3, ADDR_ROW_O, r)
        self.__spacer(4, ADDR_ROW_O, r)

        #ADDR INPUT
        sk = 0
        offset = 7
        clr = tr
        for i in range(0, 16):
            if i == 8: clr = tk
            pos = i+offset+sk
            print('%s, '%i, end='')
            self.__spacer(pos, ADDR_ROW_I, clr)
            if (i+3)%3 == 0: 
                sk += 1
                print()

        #CONTROLS 
        offset = 7
        for i in range(0, 8):
            pos = i+offset
            self.__spacer(pos, CTRL_ROW, tb)

        self.__spacer(1, CTRL_ROW, tk)
        self.__spacer(1, CTRL_ROW-2, g)

        cols, rows = self.cvc.grid_size()
        print(cols)
        print(rows)
        for col in range(cols):
            self.cvc.grid_columnconfigure(col, minsize=BOX_SZ)

        for row in range(rows):
            self.cvc.grid_rowconfigure(row, minsize=BOX_SZ)

    def __init_inputs(self):
        row_ctrl = 8
        row_addr = 6
        c = self.cvc
        # self.inputs['power'] = CtrlSwitchUD(c, 2,row_ctrl, 
        #     ctrl_clr.black, 'OFF|ON', 'POP|POWER')
        # self.inputs['runstop'] = CtrlSwitchUWD(c, 6, row_ctrl,
        #     ctrl_clr.black, 'STOP|RUN', 'STOP|RUN')
        # self.inputs['runstop'] = CtrlButton(c, 8, row_ctrl,
        #     ctrl_clr.blue, 'STEP', 'STEP')

        offset=4
        for i in range(0, 8):
            CtrlSwitchUD(c, i+offset, ADDR_ROW_I, ctrl_clr.black,'', '')
        for i in range(8, 16):
            CtrlSwitchUD(c, i+offset+2, ADDR_ROW_I, ctrl_clr.red, '', '')

    def __init_outputs(self):
        c = self.cvc
        
        self.outputs['power'] = Led(
            c, 1, CTRL_ROW-1, ctrl_clr.green, 'POWER'
        )
        self.outputs['power'] = Led(
            c, 1, ADDR_ROW_O, ctrl_clr.green, 'WAIT'
        )
        self.outputs['power'] = Led(
            c, 2, ADDR_ROW_O, ctrl_clr.green, 'HLDA'
        )
        offset=5
        for i in range(0, 8):
            Led(c, i+offset, ADDR_ROW_O, ctrl_clr.red, 'A%s'%i)
        for i in range(8, 16):
            Led(c, i+offset+2, ADDR_ROW_O, ctrl_clr.red, 'A%s'%i)


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
        self.__init_grid_dim()
        #self.__init_inputs()
        #self.__init_outputs()

    def __init__(self, scpu, smem, scmp):
        self.util = GetUtil()

        #Shared        
        self.s_cpu = scpu
        self.s_mem = smem
        self.s_cmp = scmp

        #UI setup
        self.__init_ux()
        self.util.set_trans(self.cvc)

    
        

                


