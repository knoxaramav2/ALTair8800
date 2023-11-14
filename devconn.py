

from Shared import SharedDevConn


class DevConn(SharedDevConn):

    byte            : int


    def set(self, b:int):
        self.byte = b

    def get(self):
        return self.byte


    def __init__(self):
        self.byte = 0
        