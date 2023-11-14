from tkinter import END, Canvas, Entry, Frame, Text, Tk, Toplevel
from Shared import SharedDevConn
from UI import UI
from config import Config, GetConfig
from tk_manager import GetTK


class DEV0(SharedDevConn):

    __tk:   Tk
    __ui:   UI
    __cfg:  Config
    __win:  Toplevel

    __out:  Text
    __in:   Text
    __cvc:  Canvas

    i_buffer: str = ''
    o_buffer: str = ''

    def print_output(self, msg:str):
        self.__out.configure(state='normal')
        self.__out.insert('1.0', msg+'\n')
        self.__out.configure(state='disabled')

    def read_input(self):
        msg = self.__in.get()
        self.i_buffer += msg
        self.__in.delete(0, END)
        return msg

    def signal_output(self):
        pass

    def signal_input(self, event):
        msg = self.read_input()
        self.print_output(msg)

    def set(self, byte: int):
        if byte == 0: return   
        #self.i_buffer += chr(byte)
        self.print_output(chr(byte))

    def get(self) -> int:#From Interconnect
        if len(self.o_buffer) == 0: return '\0'

        c = self.o_buffer[0]
        self.o_buffer[1:]
        return c

    def start_window(self):
        w = 500
        h = 300

        self.__win = Toplevel(self.__tk)
        self.__win.title('IO')
        self.__win.geometry(f'{w}x{h}+20+20')
        self.__win.resizable(True, False)

        f = Frame(self.__win)
        f.grid(sticky='NSEW')

        self.__out = Text(f,
                          height=15, width=70,
                          background='black',
                          foreground='lightgreen',
                          highlightthickness=2,
                          state='disabled',
                          border=2,
                          )
        
        self.__in = Entry(f,
                         #height=2,
                         #width=70,
                         background='black',
                         foreground='white',
                         highlightthickness=2,
                         borderwidth=2,
                         )
        self.__in.bind('<Return>', self.signal_input)


        self.__out.pack(expand=True, fill='x',side='top')
        self.__in.pack(expand=True, fill='x', side='bottom')
        f.pack()

        self.__win.lift()
    
    def __init__(self, ui:UI) -> None:
        self.__ui = ui
        self.__tk = GetTK()
        self.__cfg = GetConfig()

        if self.__cfg.dev0: self.start_window()
        

    