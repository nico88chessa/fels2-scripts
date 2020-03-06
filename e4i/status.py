import devmem_pkg
import time
import devmem

mem = devmem.DevMem(0x40000000,44)
print("*** PRINT REGISTERS ***")
print(mem.read(0x0, 44).hexdump(4))
print("*** PRINT STATUS ***")
a = devmem_pkg.mmap_read_word(0x40000004)
print(a)
