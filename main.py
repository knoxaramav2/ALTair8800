#altair 8800 emulator
from config import Config
from core import Machine
from ui import UI
from devtest import cycle_led_regs

cnf = Config()
machine = Machine()
ui = UI(
    machine.mem,
    machine.cpu,
    machine
)

ui.run()

if cnf.IsDevMode: cycle_led_regs(machine)
