from tkinter import Image, PhotoImage
from os import path
import pyglet
from PIL import Image, ImageTk
from defs import CTRL_XY

from util import GetUtil, Util

class RSC:

    __util = Util

    #general--------------
    fonts           : dict = {}

    #images---------------
    input_photos    : dict = {}
    output_photos   : dict = {}    
    board_img       : PhotoImage

    def __load_img(self, file:str) -> PhotoImage:
        return ImageTk.PhotoImage(
            Image.open(path.join(self.__util.rsc_uri, file))
                ,width=CTRL_XY, height=CTRL_XY)

    def __load_msc_imgs(self):
        self.board_img = self.__load_img('board.png')

    def __load_led_imgs(self):
        self.output_photos['led_on_green'] = self.__load_img('led_on_green_32.png')
        self.output_photos['led_off_green'] = self.__load_img('led_off_green_32.png')
        self.output_photos['led_on_red'] = self.__load_img('led_on_red_32.png')
        self.output_photos['led_off_red'] = self.__load_img('led_off_red_32.png')
        self.output_photos['led_on_white'] = self.__load_img('led_on_white_32.png')
        self.output_photos['led_off_white'] = self.__load_img('led_off_white_32.png')

    def __load_btn_imgs(self):
        self.input_photos['btn_up_red'] = self.__load_img('btn_up_red_32.png')
        self.input_photos['btn_down_red'] = self.__load_img('btn_down_red_32.png')
        self.input_photos['btn_up_blue'] = self.__load_img('btn_up_blue_32.png')
        self.input_photos['btn_down_blue'] = self.__load_img('btn_down_blue_32.png')

    def __load_tgl_imgs(self):
        self.input_photos['tgl_up_black'] = self.__load_img('tgl_up_black_32.png')
        self.input_photos['tgl_mid_black'] = self.__load_img('tgl_mid_black_32.png')
        self.input_photos['tgl_down_black'] = self.__load_img('tgl_down_black_32.png')
        self.input_photos['tgl_up_red'] = self.__load_img('tgl_up_red_32.png')
        self.input_photos['tgl_mid_red'] = self.__load_img('tgl_mid_red_32.png')
        self.input_photos['tgl_down_red'] = self.__load_img('tgl_down_red_32.png')
        self.input_photos['tgl_up_blue'] = self.__load_img('tgl_up_blue_32.png')
        self.input_photos['tgl_mid_blue'] = self.__load_img('tgl_mid_blue_32.png')
        self.input_photos['tgl_down_blue'] = self.__load_img('tgl_down_blue_32.png')
        self.input_photos['tgl_up_white'] = self.__load_img('tgl_up_white_32.png')
        self.input_photos['tgl_mid_white'] = self.__load_img('tgl_mid_white_32.png')
        self.input_photos['tgl_down_white'] = self.__load_img('tgl_down_white_32.png')

    def __load_fonts(self):
        pyglet.font.add_directory(self.__util.font_uri)
        self.logo_font = 'Rawhide Raw 2012'
        self.lbl_font = 'Basil Gothic NBP'


    def __init__(self):
        self.__util = GetUtil()
        self.__load_fonts()
        self.__load_btn_imgs()
        self.__load_tgl_imgs()
        self.__load_led_imgs()
        self.__load_msc_imgs()

__inst__ : RSC = None

def GetRSC():
    global __inst__
    if __inst__ is None:
        __inst__ = RSC()
    return __inst__


