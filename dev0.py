from tkinter import Label, Tk, Toplevel
from UI import UI
from config import Config, GetConfig
from tk_manager import GetTK


class DEV0:

    __tk:   Tk
    __ui:   UI
    __cfg:  Config
    __win:  Toplevel

    def start_window(self):
        self.__win = Toplevel(self.__tk)
        self.__win.title('IO')
        self.__win.geometry('300x400')
        Label(self.__win, text='Test label').pack()

    def __init__(self, ui:UI) -> None:
        self.__ui = ui
        self.__tk = GetTK()
        self.__cfg = GetConfig()

        if self.__cfg.dev0: self.start_window()
        

    