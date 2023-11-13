

from Machine import Machine
from UI import UI
from dev0 import DEV0
from hotkey import init_hotkeys


print('START')

comp = Machine()
ui = UI(comp)
d0 = DEV0(ui)

init_hotkeys(comp, ui)

ui.run()

print('STOP')


