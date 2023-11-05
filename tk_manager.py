
import tkinter as tk
from tkinter import Tk


__inst__ : Tk = None

def __init_tk__():
    global __inst__
    __inst__ = tk.Tk()

def GetTK():
    global __inst__
    if __inst__ == None:
        __init_tk__()
    return __inst__