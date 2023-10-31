

from Shared import SharedMem
from config import GetConfig


class Memory(SharedMem):

    def __init__(self):
        cfg = GetConfig()