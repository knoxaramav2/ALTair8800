
import os


class Util:

    base_uri    : str
    rsc_uri     : str
    font_uri    : str

    def __load_path(self):
        self.base_uri = os.path.dirname(__file__)
        self.rsc_uri = os.path.join(self.base_uri, 'rsc')
        self.font_uri = os.path.join(self.rsc_uri, 'fonts')

    def __init__(self) -> None:
        self.__load_path()
    
__inst__ : Util = None
def GetUtil():
    global __inst__
    if __inst__ is None:
        __inst__ = Util()
    return __inst__


