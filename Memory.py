
import numpy as np
from Shared import SharedMem
from config import GetConfig
from tk_manager import GetTK
from util import GetUtil, Util

class Memory(SharedMem):

    __util  : Util

    def set_curr_buffer(self, idx: int):
        self.__util.int_to_boolarr(self.data[idx], self.curr_data)

    def set_curr_data(self, idx:int, data:int):
        self.data[idx] = data
        self.set_curr_buffer(idx)

    def __init__(self):
        self.__util = GetUtil()
        super().__init__()