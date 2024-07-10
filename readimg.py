import os, mmap, time
from astropy.io import fits
import numpy
MAP_MASK = mmap.PAGESIZE - 1

memfile = "/dev/mem"
f= os.open(memfile, os.O_RDWR | os.O_SYNC)

def primitive_write(addr,c):
    with mmap.mmap(f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE, offset=addr & ~MAP_MASK) as m:
        m.seek(addr & MAP_MASK)
        m.write(c.to_bytes(1, byteorder='big'))

def primitive_read(addr,nbytes,size=mmap.PAGESIZE):
    with mmap.mmap(f, size, mmap.MAP_SHARED, mmap.PROT_READ, offset=addr & ~MAP_MASK) as m:
        m.seek(addr & MAP_MASK)
        return m.read(nbytes)


## LED blinking
addr = 0xA000_0004
for i in range(4):
    primitive_write(addr, 0x1<<i)
    time.sleep(0.1)

## get SN
addr = 0xA000_0020
sn =  primitive_read(0xA000_0020,2*8) 
print( sn.decode() )

print(  primitive_read(0xA000_0008,2*8).decode()  )
#print(  primitive_read(0xA000_000C,2*8)  )
temp = primitive_read(0xA000_0010,2*8)
print(  temp[0],temp[1]   ) # need to convert the second byte to decimal number
print(  primitive_read(0xA000_0020,2*8).decode()   )

#primitive_write( 0xA020_000C, 1<<24 ) ## cmos_command dummy RESET
#primitive_write( 0xA020_000C, 1<<20 ) ## cmos_command dummy RSTB
#primitive_write( 0xA020_000C, 1<<4 ) ## cmos_command dummy test
#primitive_write( 0xA020_000C, 1<<16 ) ## cmos_command dummy PCLK_EN
#primitive_write( 0xA020_000C, 1<<16 ) ## cmos_command dummy PCLK_EN

## get an image
addr = 0x4000_0000
size=1024*1024*2

data = primitive_read(addr,size,size)
data=(numpy.frombuffer(data,dtype=numpy.int16).reshape(1024,1024))
hdu = fits.PrimaryHDU(data)
hdu.header['SN']  = sn.decode()
hdu.writeto('sample.fits',overwrite=True)

os.close(f)
