from ctypes import windll, byref
from functools import partial
import os
from random import randint
from tkinter import N, W, E, S, Checkbutton, Image, Label, PhotoImage, ttk, Tk, Canvas
import tkinter as tk
from state import DisplayState
from defs import Switch, Led
from PIL import Image, ImageTk
import pyglet
pyglet.options['win32_gdi_font'] = True

class UI:
    
    root : Tk
    display_state : DisplayState
    toggles : list = []
    leds : dict = {}
    fonts : list = []

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
    _row_wait_a0 = 3
    _row_addr_sw = 8
    _row_ctrl_sw = 6
    _row_spaces = []

    _win_width = 1200
    _win_height = 550

    chromakey = '#00008B'#'#333333'

    def run(self):
        self.root.update()
        self._init_labels()

        self.root.mainloop()

    def bootup_fare(self):
        t_idx = 0
        l_idx = 0

        i = 0
        for k,v in self.leds.items():
            if k == Led.power.name: 
                continue
            
            i += 1
            self.root.after(120*i, self.update_led, k, 1)
            self.root.after(120*i+300, self.update_led, k, 0)
    
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
        
        if host.txt != '':
            print('ADJ (%s %s %s) -> (%s %s, %s %s)'%(uTxt ,x,y,ux,uy,lx,ly))

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
                text='Sense Sw. _______', fg='white', 
                background=self.chromakey,
                font=(self._lbl_font, self._lbl_font_sz)
                ).place(x=150, y=190)
        #Always right of A0 toggle
        a0y=next((x for x in self.toggles if x.name == Switch.addr0.name), None)
        Label(grid, 
                text='DATA\n\nADDRESS', fg='white',
                wraplength=1000,
                background=self.chromakey,
                font=(self._lbl_font, self._lbl_font_sz)
                ).grid(column=24, row=6)
        # Label(self.cvc,
        #       text='ALTair 8800',
        #       background=self.chromakey,
        #       fg='white',
        #       font=(self._logo_font, 10)
        # #).place(x = 10, y= self._win_height+10)
        # ).grid(column=1, row=15)

        self._spacer(grid, 1, 11)
        self._spacer(grid, 1, 12)
        self._spacer(grid, 1, 13)
        self._spacer(grid, 1, 14)


    def toggle_switch(self, toggle:str):
        val = self.display_state.switches[toggle]
        print('Toggle : '+toggle +' '+str(val.get()))

        match toggle:
            case Switch.on_off.name:
                pwer = val.get()
                self.update_led(Led.power.name, pwer)
                if pwer == 1 : self.bootup_fare()
            case _:
                pass

    def update_led(self, name, state):
        led = self.leds[name]
        if state == 1:
            led.configure(image=led.clr_on)
        else:
            led.configure(image=led.clr_off)

    def _create_led(self, grid, col, row, name, txt='', clr='red'):

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

        led = Label(
            grid, #text=name,
            fg='white',
            image=clr_off,
            highlightthickness=0, bd=0, border=0,
            bg=self.chromakey
        )
        led.grid(
            column=col, row=row,
            padx=10, sticky=(W,S,E,N)
        )
        led.txt = txt
        led.clr_on = clr_on,
        led.clr_off = clr_off
        self.leds[name] = led

    def _create_toggle(self, grid, col, row, name, txt='', clr='black'):

        clr_up = self.img_tgl_up_black
        clr_down = self.img_tgl_down_black

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
            case _:
                pass

        tgl = Checkbutton(
            grid, #text=name,
            fg='white',
            indicatoron=False,
            selectimage=clr_up,
            image=clr_down,
            command=partial(self.toggle_switch, name),
            variable=self.display_state.switches[name],
            highlightthickness=0, bd=0, border=0,
            bg=self.chromakey, selectcolor=self.chromakey, 
            activebackground=self.chromakey, activeforeground='white'
        )
        tgl.grid(
            column=col, row=row, 
            padx=10, sticky=(W, S, E, N))
        tgl.name = name
        tgl.txt = txt
        self.toggles.append(tgl)
    #c, r
    def _init_toggles(self, grid):
        rc = self._row_ctrl_sw
        ra = self._row_addr_sw

        self._spacer(grid, 1, 9)
        self._spacer(grid, 1, 10)
        self._create_toggle(grid, 1, 8, Switch.on_off.name, 'OFF|ON', 'blue')
        self._spacer(grid, 2, 8)
        self._create_toggle(grid, 6, 8, Switch.stop_run.name, 'STOP|RUN')
        self._create_toggle(grid, 8, 8, Switch.single_step.name, 'SINGLE STEP')
        self._create_toggle(grid, 10, 8, Switch.examine.name, 'EXAMINE|EXAMINE NEXT')
        self._create_toggle(grid, 12, 8, Switch.deposit.name, 'DEPOSIT|DEPOSIT NEXT')
        self._create_toggle(grid, 14, 8, Switch.reset_clr.name,'RESET|CLR')
        self._create_toggle(grid, 16, 8, Switch.prtct_unprtct.name, 'PROTECT|UNPROTECT')
        self._create_toggle(grid, 18, 8, Switch.aux1.name, 'AUX1')
        self._create_toggle(grid, 20, 8, Switch.aux2.name, 'AUX2')

        self._spacer(grid, 2, 7)

        self._create_toggle(grid, 6, 6, Switch.addr15.name, '15', 'red')
        self._create_toggle(grid, 7, 6, Switch.addr14.name, '14', 'red')
        self._create_toggle(grid, 8, 6, Switch.addr13.name, '13', 'red')
        self._create_toggle(grid, 9, 6, Switch.addr12.name, '12', 'red')
        self._create_toggle(grid, 10, 6, Switch.addr11.name, '11', 'red')
        self._create_toggle(grid, 11, 6, Switch.addr10.name, '10', 'red')
        self._create_toggle(grid, 12, 6, Switch.addr9.name, '9', 'red')
        self._create_toggle(grid, 13, 6, Switch.addr8.name, '8', 'red')
        self._create_toggle(grid, 16, 6, Switch.addr7.name, '7', 'white')
        self._create_toggle(grid, 17, 6, Switch.addr6.name, '6', 'white')
        self._create_toggle(grid, 18, 6, Switch.addr5.name, '5', 'white')
        self._create_toggle(grid, 19, 6, Switch.addr4.name, '4', 'white')
        self._create_toggle(grid, 20, 6, Switch.addr3.name, '3', 'white')
        self._create_toggle(grid, 21, 6, Switch.addr2.name, '2', 'white')
        self._create_toggle(grid, 22, 6, Switch.addr1.name, '1', 'white')
        self._create_toggle(grid, 23, 6, Switch.addr0.name, '0', 'white')

        self._spacer(grid, 1, 5)
        self._spacer(grid, 1, 4)
        self._spacer(grid, 24, 6)

    def _init_leds(self, grid):
        self._create_led(grid, 1, 6, Led.power.name, 'POWER', 'green')
        self._create_led(grid, 3, 3, Led.wait.name, 'WAIT')
        self._create_led(grid, 4, 3, Led.hlda.name, 'HLDA')

        self._create_led(grid, 6, 3, Led.a15.name, 'A15')
        self._create_led(grid, 7, 3, Led.a14.name, 'A14')
        self._create_led(grid, 8, 3, Led.a13.name, 'A13')
        self._create_led(grid, 9, 3, Led.a12.name, 'A12')
        self._create_led(grid, 10, 3, Led.a11.name, 'A11')
        self._create_led(grid, 11, 3, Led.a10.name, 'A10')
        self._create_led(grid, 12, 3, Led.a9.name, 'A9')
        self._create_led(grid, 13, 3, Led.a8.name, 'A8')
        self._spacer(grid, 14, 3)
        self._spacer(grid, 15, 3)
        self._create_led(grid, 16, 3, Led.a7.name, 'A7')
        self._create_led(grid, 17, 3, Led.a6.name, 'A6')
        self._create_led(grid, 18, 3, Led.a5.name, 'A5')
        self._create_led(grid, 19, 3, Led.a4.name, 'A4')
        self._create_led(grid, 20, 3, Led.a3.name, 'A3')
        self._create_led(grid, 21, 3, Led.a2.name, 'A2')
        self._create_led(grid, 22, 3, Led.a1.name, 'A1')
        self._create_led(grid, 23, 3, Led.a0.name, 'A0')

        self._spacer(grid, 1, 2)

        self._create_led(grid, 3, 1, Led.inte.name, 'INTE')
        self._create_led(grid, 4, 1, Led.prot.name, 'PROT')
        self._create_led(grid, 5, 1, Led.memr.name, 'MEMR')
        self._create_led(grid, 6, 1, Led.inp.name, 'INP')
        self._create_led(grid, 7, 1, Led.m1.name, 'M1')
        self._create_led(grid, 8, 1, Led.out.name, 'OUT')
        self._create_led(grid, 9, 1, Led.hlta.name, 'MLTA')
        self._create_led(grid, 10, 1, Led.stack.name, 'STACK')
        self._create_led(grid, 11, 1, Led.wo.name, 'WO')
        self._create_led(grid, 12, 1, Led.int.name, 'INT')

        self._create_led(grid, 16, 1, Led.d7.name, 'D7')
        self._create_led(grid, 17, 1, Led.d6.name, 'D6')
        self._create_led(grid, 18, 1, Led.d5.name, 'D5')
        self._create_led(grid, 19, 1, Led.d4.name, 'D4')
        self._create_led(grid, 20, 1, Led.d3.name, 'D3')
        self._create_led(grid, 21, 1, Led.d2.name, 'D2')
        self._create_led(grid, 22, 1, Led.d1.name, 'D1')
        self._create_led(grid, 23, 1, Led.d0.name, 'D0')

        self._spacer(grid, 1, 0)

    def _init_consts(self):
        self._base_dir = os.path.dirname(__file__)
        self._rsc_dir = os.path.join(self._base_dir, 'rsc')
        self._font_dir = os.path.join(self._rsc_dir, 'fonts')


    def _trans(self, c):
        hwnd =c.winfo_id()
        wnd_exstyle = windll.user32.GetWindowLongA(hwnd, -20)  # GWL_EXSTYLE
        new_exstyle = wnd_exstyle | 0x00080000  # WS_EX_LAYERED
        windll.user32.SetWindowLongA(hwnd, -20, new_exstyle)  # GWL_EXSTYLE
        windll.user32.SetLayeredWindowAttributes(hwnd, 0x008B0000, 255, 0x00000001)

    def _load_imgs(self):
        base = self._rsc_dir

        self.img_panel_dark = ImageTk.PhotoImage(
            Image.open(os.path.join(base, 'board.png'))
            ,width=self._win_width, height=self._win_height)

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

    def __init__(self):
        self.root = tk.Tk()
        self.display_state = DisplayState()

        self._init_consts()
        self._load_imgs()
        self._load_fonts()

        r = self.root
        r.title('Altair Emu')
        r.geometry('%sx%s'%(self._win_width, self._win_height))
        #r.resizable(False, False)
        r.configure(background='grey')
        print(r.cget('bg'))
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
        self._trans(self.cvc)




        


