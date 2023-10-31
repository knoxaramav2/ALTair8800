class SharedMemory:
    heap = []
    stack = []

    def set_heap(self, idx, data):
        self.heap[idx] = data


class SharedChip:
    inst_ptr        : int   #16 bit
    mem_bffr_ptr    : int   #16 bit

class SharedMachine:
    power_on = False