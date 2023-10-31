

from Machine import Machine
from UI import UI

print('START')

comp = Machine()
ui = UI(
    comp.cpu,
    comp.mem,
    comp
)

print('STOP')


