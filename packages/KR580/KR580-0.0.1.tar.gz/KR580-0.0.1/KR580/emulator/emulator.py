import ctypes as c
import os

#lib_emul = c.cdll.LoadLibrary('./CPU.so')
lib_path = os.path.dirname(os.path.abspath(__file__)) + '/CPU.so'
lib_emul = c.cdll.LoadLibrary(lib_path)

class cpu_t(c.Structure):
    _fields_ = [
    ('registers', c.c_uint8 * 0x8),
    ('flags', c.c_bool * 0x5),
    ('memory', c.c_uint8 * 0xffff),
    ('stack', c.c_uint8 * 0xffff),
    ('program_counter', c.c_uint16),
    ('stack_pointer', c.c_uint16),
    ('tick_counter', c.c_uint32),
    ('memory_pointer', c.c_uint16),
    ('interrupts_enabled', c.c_bool)]

    def write_memory(self, start, memory):
        for i, cell in enumerate(memory):
            self.memory[start+i] = cell

    def execute(self):
        lib_emul.execute(c.byref(self))
        print(self.registers[0])

cpu_p = c.POINTER(cpu_t)

lib_emul.init_cpu.argtypes = [c.POINTER(c.c_uint8), c.c_uint16, c.c_uint16]
lib_emul.init_cpu.restype = cpu_t
lib_emul.execute_command.argtypes = [cpu_p, c.c_uint8]
lib_emul.execute.argtypes = [cpu_p]

def init_cpu(codes, start=0x1000):
    mem_len = len(codes)
    mem = (c.c_uint8 * mem_len)(*codes)
    mem = c.cast(mem, c.POINTER(c.c_uint8))
    cpu = lib_emul.init_cpu(mem, mem_len, start)
    return cpu
