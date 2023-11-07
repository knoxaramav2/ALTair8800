

from Machine import Machine
from UI import UI
from hotkey import init_hotkeys


print('START')

comp = Machine()
ui = UI(comp)

init_hotkeys(comp)

ui.run()

print('STOP')


