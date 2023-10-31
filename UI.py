

from Shared import SharedCPU, SharedMachine, SharedMem


class UI:

    #Shared Memory
    s_cpu       : SharedCPU
    s_mem       : SharedMem
    s_cmp       : SharedMachine


    def __init__(self,
                 scpu, smem, scmp
                 ) -> None:
        
        self.s_cpu = scpu
        self.s_mem = smem
        self.s_cmp = scmp



