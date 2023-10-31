from ctypes import windll
import os
from random import randint
from tkinter import N, W, E, S, Checkbutton, Image, IntVar, Label, PhotoImage, Radiobutton, Tk, Canvas
import tkinter as tk
from defs import Switch, Led
from PIL import Image, ImageTk
import pyglet
from shared import *


pyglet.options['win32_gdi_font'] = True

class UI:
    
    root : Tk
    toggles : list = []
    toggle_states : dict = {}
    leds : dict = {}
    fonts : list = []

    #Shared components
    shr_mem : SharedMemory
    shr_chip : SharedChip
    shr_comp : SharedMachine

    img_btn_up_red : PhotoImage
    img_btn_down_red : PhotoImage
    img_btn_up_blue : PhotoImage
    img_btn_down_blue : PhotoImage
    img_tgl_up_black : PhotoImage
    img_tgl_down_black : PhotoImage
    img_tgl_up_red : PhotoImage
    img_tgl_down_red : PhotoImage
    img_tgl_up_green : PhotoImage
    img_tgl_down_green : PhotoImage
    img_tgl_up_blue : PhotoImage
    img_tgl_down_blue : PhotoImage
    img_tgl_up_white : PhotoImage
    img_tgl_down_white : PhotoImage
    img_led_on_red : PhotoImage
    img_led_off_red : PhotoImage
    img_led_on_green : PhotoImage
    img_led_off_green : PhotoImage
    img_led_on_white : PhotoImage
    img_led_off_white : PhotoImage
    img_panel_dark : PhotoImage

    cvc : Canvas
    clb : Canvas

    _logo_font : str
    _lbl_font : str
    _lbl_font_sz : int = 10
    _base_dir : str
    _rsc_dir : str
    _font_dir : str

    #row specifiers
    _row_inte_d0 = 1
    _row_wait_a0 = 4
    _row_addr_sw = 6
    _row_ctrl_sw = 8
    _row_spaces = [0,2,3,5,7,9,10]

    _win_width = 1200
    _win_height = 550

    chromakey = '#00008B'

    def run(self):
        self.root.update()
        self._init_labels()
        self.root.mainloop()

    #UI UDX Controls

    def ui_power(self):
        self.shr_comp.power_on = 1 - self.shr_comp.power_on
        print('POWER: %s'%self.shr_comp.power_on)

    def ui_stop_run(self):
        pass

    def ui_single_step(self):
        pass

    def ui_examine(self):
        pass

    def ui_deposit(self):
        pass

    def ui_deposit(self):
        pass

    def ui_reset(self):
        pass

    def ui_protect(self):
        pass

    def ui_aux(self):
        pass

    def ui_data_addr(self):
        pass

    
    #Misc. UI methods
    def pop(self, name):
        pass

    #adj_y due to toggle/led height difference
    def _init_label(self, grid, host, x, y, adj_y=0):
        split = host.txt.split('|')
        uTxt = split[0]
        lTxt = split[1] if '|' in host.txt else ''
        #all toggle, led imgs assumed same size
        #TODO make more dynamic
        w = self.img_tgl_down_black.width()
        h = self.img_tgl_down_black.height()
        #attempt to auto center text
        #TODO get pixel length directly to support
        #custom fonts
        cx = 4.8#pixels per char
        ux = x+((w-(len(uTxt)*cx))/2)
        uy = y+adj_y
        lx = x+((w-(len(lTxt)*cx))/2)
        ly = y+50+adj_y

        ulbl = Label(grid, text=uTxt,
            highlightthickness=0, bd=0, border=0,
            wraplength=200,
            bg=self.chromakey, 
            font=(self._lbl_font, self._lbl_font_sz),
            fg='white').place(x=ux, y=uy)
        dlbl = Label(grid, text=lTxt,
            highlightthickness=0, bd=0, border=0,
            wraplength=200,
            bg=self.chromakey,
            font=(self._lbl_font, self._lbl_font_sz),
            fg='white').place(x=lx, y=ly)
        host.ulabel = ulbl
        host.dlabel = dlbl

        a = Checkbutton()
        pass

    def _init_labels(self):
        grid = self.cvc
        for n in self.toggles:
            x = n.winfo_x()
            y = n.winfo_y()
            self._init_label(
                self.cvc, n, x, y
            )

        for k, n in self.leds.items():
            x = n.winfo_x()
            y = n.winfo_y()
            self._init_label(
                self.cvc, n, x, y, -20
            )

        Label(grid, 
                text='STATUS', fg='white',
                background=self.chromakey,
                font=(self._lbl_font, self._lbl_font_sz)
                ).grid(column=8, row=self._row_inte_d0+1)

        Label(grid, 
                text='Sense Sw. _______', fg='white', 
                background=self.chromakey,
                font=(self._lbl_font, self._lbl_font_sz)
                ).place(x=150, y=190)
        Label(grid, 
                text='DATA\n\nADDRESS', fg='white',
                wraplength=1000,
                background=self.chromakey,
                font=(self._lbl_font, self._lbl_font_sz)
                ).grid(column=24, row=self._row_addr_sw)

        self._spacer(grid, 1, 11)
        self._spacer(grid, 1, 12)
        self._spacer(grid, 1, 13)
        self._spacer(grid, 1, 14)

    def update_led(self, name, state):
        led = self.leds[name]
        if state == 1:
            led.configure(image=led.clr_on)
        else:
            led.configure(image=led.clr_off)

    def _create_led(self, grid, col:int, row:int, name:str, vrst:bool=None, txt:str='', clr:str='red'):

        clr_on = self.img_led_on_red
        clr_off = self.img_led_off_red

        match clr:
            case 'green':
                clr_on = self.img_led_on_green
                clr_off = self.img_led_off_green
            case 'white':
                clr_on = self.img_led_on_white
                clr_off = self.img_led_off_white
            case _:
                pass

        # led = Label(
        #     grid,
        #     fg='white',
        #     image=clr_off,
        #     highlightthickness=0, bd=0, border=0,
        #     bg=self.chromakey
        # )
        led = Radiobutton(
            grid,
            state='disabled',
            fg='white',
            indicatoron=False,
            image=clr_off,
            selectimage=clr_on,
            variable=vrst,
            highlightthickness=0, bd=0, border=0,
            bg=self.chromakey,
            selectcolor=self.chromakey,
            activebackground=self.chromakey
        )
        led.grid(
            column=col, row=row,
            padx=10, sticky=(W,S,E,N)
        )
        led.txt = txt
        led.clr_on = clr_on,
        led.clr_off = clr_off
        self.leds[name] = led

    def _group_lambdas(self, fncs):
        def fnc(*args, **kwargs):
            for f in fncs:
                f(*args, **kwargs)
        return fnc

    def _create_toggle(self, grid, col, row, name, txt='', clr='black', cmd=''):

        clr_up = self.img_tgl_up_black
        clr_down = self.img_tgl_down_black
        commands = []

        match clr:
            case 'red':
                clr_up = self.img_tgl_up_red
                clr_down = self.img_tgl_down_red
            case 'blue':
                clr_up = self.img_tgl_up_blue
                clr_down = self.img_tgl_down_blue
            case 'white':
                clr_up = self.img_tgl_up_white
                clr_down = self.img_tgl_down_white
            case 'green':
                clr_up = self.img_tgl_up_green
                clr_down = self.img_tgl_down_green
            #Reversed for buttons
            case 'btn_blue':
                clr_down = self.img_btn_up_blue
                clr_up = self.img_btn_down_blue
            case 'btn_red':
                clr_down = self.img_btn_up_red
                clr_up = self.img_btn_down_red
            case _:
                pass

        for c in cmd.split('|'):
            if c == 'pop': commands.append(lambda:self.root.after(1000, self.pop, name))
            elif c == 'power': commands.append(lambda:self.root.after(1000, self.ui_power))
            elif c == 'runstop': commands.append(lambda:self.root.after(1000, self.ui_stop_run))
            elif c == 'step': commands.append(lambda:self.root.after(1000, self.ui_single_step))
            elif c == 'examine': commands.append(lambda:self.root.after(1000, self.ui_examine))
            elif c == 'deposit': commands.append(lambda:self.root.after(1000, self.ui_deposit))
            elif c == 'reset': commands.append(lambda:self.root.after(1000, self.ui_reset))
            elif c == 'protect': commands.append(lambda:self.root.after(1000, self.ui_protect))
            elif c == 'tgl_aux': commands.append(lambda:self.root.after(1000, self.ui_aux))
            elif c == 'addr': commands.append(lambda:self.root.after(1000, self.ui_data_addr))

        tgl = Checkbutton(
            grid, #text=name,
            fg='white',
            indicatoron=False,
            selectimage=clr_up,
            image=clr_down,
            variable=self.toggle_states[name],
            highlightthickness=0, bd=0, border=0,
            bg=self.chromakey, selectcolor=self.chromakey, 
            activebackground=self.chromakey, activeforeground='white'
        )
        tgl.grid(
            column=col, row=row, 
            padx=10, sticky=(W, S, E, N))
        if cmd != '': tgl.configure(command=self._group_lambdas(commands))
        tgl.name = name
        tgl.txt = txt
        self.toggles.append(tgl)

    def _init_toggles(self, grid):
        rc = self._row_ctrl_sw
        ra = self._row_addr_sw

        self._create_toggle(grid, 1, rc, Switch.on_off.name, 'OFF|ON', 'white', 'power')
        self._spacer(grid, 2, 8)
        self._create_toggle(grid, 6, rc, Switch.stop_run.name, 'STOP|RUN', 'btn_blue', 'runstop')
        self._create_toggle(grid, 8, rc, Switch.single_step.name, 'SINGLE STEP', 'btn_blue', 'step|pop')
        self._create_toggle(grid, 10, rc, Switch.examine.name, 'EXAMINE|EXAMINE NEXT', 'btn_blue', 'examine')
        self._create_toggle(grid, 12, rc, Switch.deposit.name, 'DEPOSIT|DEPOSIT NEXT', 'btn_blue', 'deposit')
        self._create_toggle(grid, 14, rc, Switch.reset_clr.name,'RESET|CLR', 'btn_blue', 'reset|pop')
        self._create_toggle(grid, 16, rc, Switch.prtct_unprtct.name, 'PROTECT|UNPROTECT', 'btn_blue', 'protect')
        self._create_toggle(grid, 18, rc, Switch.aux1.name, 'AUX1', cmd='tgl_aux')
        self._create_toggle(grid, 20, rc, Switch.aux2.name, 'AUX2', cmd='tgl_aux')
        self._create_toggle(grid, 6, ra, Switch.addr15.name, '15', 'red', cmd='addr')
        self._create_toggle(grid, 7, ra, Switch.addr14.name, '14', 'red', cmd='addr')
        self._create_toggle(grid, 8, ra, Switch.addr13.name, '13', 'red', cmd='addr')
        self._create_toggle(grid, 9, ra, Switch.addr12.name, '12', 'red', cmd='addr')
        self._create_toggle(grid, 10, ra, Switch.addr11.name, '11', 'red', cmd='addr')
        self._create_toggle(grid, 11, ra, Switch.addr10.name, '10', 'red', cmd='addr')
        self._create_toggle(grid, 12, ra, Switch.addr9.name, '9', 'red', cmd='addr')
        self._create_toggle(grid, 13, ra, Switch.addr8.name, '8', 'red', cmd='addr')
        self._create_toggle(grid, 16, ra, Switch.addr7.name, '7', 'white', cmd='addr')
        self._create_toggle(grid, 17, ra, Switch.addr6.name, '6', 'white', cmd='addr')
        self._create_toggle(grid, 18, ra, Switch.addr5.name, '5', 'white', cmd='addr')
        self._create_toggle(grid, 19, ra, Switch.addr4.name, '4', 'white', cmd='addr')
        self._create_toggle(grid, 20, ra, Switch.addr3.name, '3', 'white', cmd='addr')
        self._create_toggle(grid, 21, ra, Switch.addr2.name, '2', 'white', cmd='addr')
        self._create_toggle(grid, 22, ra, Switch.addr1.name, '1', 'white', cmd='addr')
        self._create_toggle(grid, 23, ra, Switch.addr0.name, '0', 'white', cmd='addr')
        self._spacer(grid, 24, 6)

    def _init_leds(self, grid):
        ra = self._row_wait_a0
        rs = self._row_inte_d0
        addr = self.shr_chip.inst_ptr
        data = self.shr_chip.mem_bffr_ptr

        self._create_led(grid, 1, 6, Led.power.name, self.shr_comp.power_on, 'POWER', 'green')
        self._create_led(grid, 3, ra, Led.wait.name, None, 'WAIT')
        self._create_led(grid, 4, ra, Led.hlda.name, None, 'HLDA')

        self._create_led(grid, 6, ra, Led.a15.name, addr&0x10, 'A15')
        self._create_led(grid, 7, ra, Led.a14.name, addr&0xF, 'A14')
        self._create_led(grid, 8, ra, Led.a13.name, addr&0xE, 'A13')
        self._create_led(grid, 9, ra, Led.a12.name, addr&0xD, 'A12')
        self._create_led(grid, 10, ra, Led.a11.name, addr&0xC, 'A11')
        self._create_led(grid, 11, ra, Led.a10.name, addr&0xB, 'A10')
        self._create_led(grid, 12, ra, Led.a9.name, addr&0xA, 'A9')
        self._create_led(grid, 13, ra, Led.a8.name, addr&0x9, 'A8')
        self._spacer(grid, 14, 3)
        self._spacer(grid, 15, 3)
        self._create_led(grid, 16, ra, Led.a7.name, addr&0x8, 'A7')
        self._create_led(grid, 17, ra, Led.a6.name, addr&0x7, 'A6')
        self._create_led(grid, 18, ra, Led.a5.name, addr&0x6, 'A5')
        self._create_led(grid, 19, ra, Led.a4.name, addr&0x5, 'A4')
        self._create_led(grid, 20, ra, Led.a3.name, addr&0x4, 'A3')
        self._create_led(grid, 21, ra, Led.a2.name, addr&0x3, 'A2')
        self._create_led(grid, 22, ra, Led.a1.name, addr&0x2, 'A1')
        self._create_led(grid, 23, ra, Led.a0.name, addr&0x1, 'A0')
        self._create_led(grid, 3, rs, Led.inte.name, None, 'INTE')
        self._create_led(grid, 4, rs, Led.prot.name, None, 'PROT')
        self._create_led(grid, 5, rs, Led.memr.name, None, 'MEMR')
        self._create_led(grid, 6, rs, Led.inp.name, None, 'INP')
        self._create_led(grid, 7, rs, Led.m1.name, None, 'M1')
        self._create_led(grid, 8, rs, Led.out.name, None, 'OUT')
        self._create_led(grid, 9, rs, Led.hlta.name, None, 'MLTA')
        self._create_led(grid, 10, rs, Led.stack.name, None, 'STACK')
        self._create_led(grid, 11, rs, Led.wo.name, None, 'WO')
        self._create_led(grid, 12, rs, Led.int.name, None, 'INT')

        self._create_led(grid, 16, rs, Led.d7.name, data&0x8, 'D7')
        self._create_led(grid, 17, rs, Led.d6.name, data&0x7, 'D6')
        self._create_led(grid, 18, rs, Led.d5.name, data&0x6, 'D5')
        self._create_led(grid, 19, rs, Led.d4.name, data&0x5, 'D4')
        self._create_led(grid, 20, rs, Led.d3.name, data&0x4, 'D3')
        self._create_led(grid, 21, rs, Led.d2.name, data&0x3, 'D2')
        self._create_led(grid, 22, rs, Led.d1.name, data&0x2, 'D1')
        self._create_led(grid, 23, rs, Led.d0.name, data&0x1, 'D0')

    def _init_consts(self):
        self._base_dir = os.path.dirname(__file__)
        self._rsc_dir = os.path.join(self._base_dir, 'rsc')
        self._font_dir = os.path.join(self._rsc_dir, 'fonts')


    def _trans(self, c):
        hwnd = c.winfo_id()
        wnd_exstyle = windll.user32.GetWindowLongA(hwnd, -20)  # GWL_EXSTYLE
        new_exstyle = wnd_exstyle | 0x00080000  # WS_EX_LAYERED
        windll.user32.SetWindowLongA(hwnd, -20, new_exstyle)  # GWL_EXSTYLE
        windll.user32.SetLayeredWindowAttributes(hwnd, 0x008B0000, 255, 0x00000001)

    def _load_imgs(self):
        base = self._rsc_dir

        self.img_panel_dark = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'board.png'))
            ,width=self._win_width, height=self._win_height)

        #Buttons
        self.img_btn_down_blue = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'btn_down_blue_32.png'))
                ,width=20, height=20)
        self.img_btn_up_blue = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'btn_up_blue_32.png'))
                ,width=20, height=20)
        self.img_btn_down_red = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'btn_down_red_32.png'))
                ,width=20, height=20)
        self.img_btn_up_red = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'btn_up_red_32.png'))
                ,width=20, height=20)
        #Toggles
        self.img_tgl_down_black = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_down_black_32.png'))
                ,width=20, height=20)
        self.img_tgl_up_black = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_up_black_32.png'))
                ,width=20, height=20)
        self.img_tgl_down_red = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_down_red_32.png'))
                ,width=20, height=20)
        self.img_tgl_up_red = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_up_red_32.png'))
                ,width=20, height=20)
        self.img_tgl_down_green = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_down_green_32.png'))
                ,width=20, height=20)
        self.img_tgl_up_green = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_up_green_32.png'))
                ,width=20, height=20)
        self.img_tgl_down_white = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_down_white_32.png'))
                ,width=20, height=20)
        self.img_tgl_up_white = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_up_white_32.png'))
                ,width=20, height=20)
        self.img_tgl_down_blue = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_down_blue_32.png'))
                ,width=20, height=20)
        self.img_tgl_up_blue = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'toggle_up_blue_32.png'))
                ,width=20, height=20)
        
        #LEDS
        self.img_led_on_red = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'led_on_red_32.png'))
                ,width=20, height=20)
        self.img_led_off_red = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'led_off_red_32.png'))
                ,width=20, height=20)
        self.img_led_on_white = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'led_on_white_32.png'))
                ,width=20, height=20)
        self.img_led_off_white = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'led_off_white_32.png'))
                ,width=20, height=20)
        self.img_led_on_green = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'led_on_green_32.png'))
                ,width=20, height=20)
        self.img_led_off_green = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'led_off_green_32.png'))
                ,width=20, height=20)

    def _load_fonts(self):
        pyglet.font.add_directory(self._font_dir)
        self._logo_font = 'Rawhide Raw 2012'
        self._lbl_font = 'Basil Gothic NBP'

    def _spacer(self, grid, col=0, row = 0):
        Label(grid, bd=0, borderwidth=0, 
              highlightthickness=0, 
              bg=self.chromakey).grid(row=row, column=col, pady=5)

    def _add_spacers(self, grid):
        for row in self._row_spaces:
            self._spacer(grid, 1, row)

    def _init_states(self):
        for s in Switch:
            self.toggle_states[s.name] = IntVar(value=0)
        self.toggle_states[Switch.on_off] = True

    def __init__(self,
                    shr_mem:SharedMemory,
                    shr_chp:SharedChip,
                    shr_comp:SharedMachine
                 ):
        self.root = tk.Tk()

        self.shr_mem = shr_mem
        self.shr_chip = shr_chp
        self.shr_comp = shr_comp
        
        self._init_consts()
        self._load_imgs()
        self._load_fonts()
        self._init_states()

        r = self.root
        r.title('Altair Emu')
        r.geometry('%sx%s'%(self._win_width, self._win_height))
        r.resizable(False, False)
        r.configure(background='grey')
        r.grid_columnconfigure(0, weight=1, pad=50)
        r.grid_rowconfigure(0, weight=1, pad=50)

        bgp = Label(self.root, image=self.img_panel_dark)
        bgp.place(x=0, y=0, width=self._win_width, height=self._win_height)

        self.cvc = tk.Canvas(r, background=self.chromakey,
                             width=self._win_width,
                             height=self._win_height+1200,
                            bd=0, border=0, highlightthickness=0, relief='ridge')
        self.cvc.grid(row=0, column=0, pady=10, sticky='NW')

        self._init_leds(self.cvc)
        self._init_toggles(self.cvc)
        self._add_spacers(self.cvc)
        self._trans(self.cvc)
