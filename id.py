import os, mmap, time
MAP_MASK = mmap.PAGESIZE - 1
addr = 0xA000_0020

f= os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
with mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ, offset=addr & ~MAP_MASK) as m:
    m.seek(addr & MAP_MASK)
    print(f"{addr:x}: ", m.read(16))

os.close(f)
