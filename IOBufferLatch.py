
from Shared import SharedDevConn, SharedIOBuffLatch
from devconn import DevConn


class IOBufferLatch(SharedIOBuffLatch):

    __devs              : [SharedDevConn]
    __dev_lim           : int

    def __init_connections(self, dev_count:int):
        self.__devs = [DevConn] * dev_count
        for d in self.__devs:
            d = None

    def connect(self, dev_no:int, dev: SharedDevConn):
        if dev_no >= dev_no:
            print(f'Device No. exceeds limit. (LIMIT={self.__dev_lim})')
            return
        if self.__devs[dev_no] != None:
            print(f'Cannot connect Dev. No. {dev_no}. IN USE')
            return
        
        self.__devs[dev_no] = dev

    def disconnect(self, dev_no:int):
        if dev_no >= dev_no:
            print(f'Device No. exceeds limit. (LIMIT={self.__dev_lim})')
            return
        if self.__devs[dev_no] != None:
            print(f'Dev. No {dev_no} not connected.')
            return
        
        self.__devs[dev_no] = None

    def write(self, addr: int, byte: int):
        if addr >= self.__dev_lim or self.__devs[addr] == None:
            print(f'Cannot write to Dev. No {addr}')
            return
        self.__devs[addr].set(byte)

    def read(self, addr:int):
        if addr >= self.__dev_lim or self.__devs[addr] == None:
            print(f'Cannot read from Dev. No {addr}')
            return
        return self.__devs[addr].get()

    def __init__(self, dev_count:int):
        self.__dev_lim = dev_count
        self.__init_connections(dev_count)

