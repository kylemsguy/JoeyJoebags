def BV_SetBank(dev, blk, sublk):  # 1-4:1-4
    # Lock cart before writing
    sublk = sublk * 64
    print(hex(blk), hex(sublk))
    dev.write(0x01, [0x0A, 0x00, 0x03, 0x70, 0x00, sublk, 0x70,
              0x01, 0xE0, 0x70, 0x02, blk])  # Lock flash block
    USBbuffer = dev.read(0x81, 64)


def ROMBankSwitch(dev, bankNumber):
    # Convert 16bit bank number to 2 x 8bit numbers
    # Write to address defined under MBC settings to swap banks. This will change depending on certain cart types...
    bhi = bankNumber >> 8
    blo = bankNumber & 0xFF
    # if bhi > 0:
    dev.write(0x01, [0x0A, 0x00, 0x01, 0x30, 0x00, bhi])
    USBbuffer = dev.read(0x81, 64)
    dev.write(0x01, [0x0A, 0x00, 0x01, 0x21, 0x00, blo])
    USBbuffer = dev.read(0x81, 64)