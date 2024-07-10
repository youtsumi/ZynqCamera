import os, mmap, time
MAP_MASK = mmap.PAGESIZE - 1
addr = 0xA000_0004

f= os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
with mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ, offset=addr & ~MAP_MASK) as m:

    print(f"{addr & ~MAP_MASK:x}")
    for i in range(4):
        m.seek(addr & MAP_MASK)
        m.write((1 << i).to_bytes(1, byteorder='big'))
        time.sleep(0.1)

os.close(f)
