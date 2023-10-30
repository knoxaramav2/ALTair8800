#altair 8800 emulator
from config import Config
from core import Machine
from devtest import cycle_led_regs
from mem import Memory
from chip8080 import Chip8080
cnf = Config()
machine = Machine()

if cnf.IsDevMode: cycle_led_regs()

machine.Start()
