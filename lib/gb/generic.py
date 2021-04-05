from .header import GBHeader
from .common import BV_SetBank, ROMBankSwitch, RAMBankSwitch

# MBC code goes here...

def read_cart_header(dev):
    BV_SetBank(dev, 0, 0)
    ROMBankSwitch(dev, 1)
    RAMtypes = [0, 2048, 8192, 32768, (32768*4), (32768*2)]
    header = ""
    dev.write(0x01, [0x10, 0x00, 0x00, 0x01, 0x00])  # start of logo
    dat = dev.read(0x81, 64)
    header = dat
    msg = [0x10, 0x00, 0x00, 0x01, 0x40]
    dev.write(0x01, msg)
    dat = dev.read(0x81, 64)
    header += dat
    msg = [0x10, 0x00, 0x00, 0x01, 0x80]
    dev.write(0x01, msg)
    dat = dev.read(0x81, 64)
    header += dat  # Header contains 0xC0 bytes of header data

    header_obj = GBHeader(header)
    return header_obj


def dump_rom(dev, ROMsize, BankSize, outfile):
    ROMbuffer = ""
    num_banks = ROMsize // BankSize
    for bankNumber in range(num_banks):
        print('Dumping ROM:', int(bankNumber*BankSize), ' of ', ROMsize)
        if bankNumber == 0:
            # get bank 0 from address 0, not setbank(0) and get from high bank...
            ROMaddress = 0
        else:
            ROMaddress = BankSize
        ROMBankSwitch(dev, bankNumber)  # switch to new bank.
        packets = int(BankSize/64)
        for packetNumber in range(packets):
            AddHi = ROMaddress >> 8
            AddLo = ROMaddress & 0xFF
            dev.write(0x01, [0x10, 0x00, 0x00, AddHi, AddLo])
            ROMbuffer = dev.read(0x81, 64)
            outfile.write(ROMbuffer)
            ROMaddress += 64


def dump_ram(dev, RAMsize, BankSize):
    RAMbuffer = []
    num_banks = RAMsize // 8192
    for bankNumber in range(num_banks):
        RAMaddress = 0xA000
        RAMBankSwitch(dev, bankNumber)
        num_packets = 8192 // 64
        for packetNumber in range(num_packets):
            AddHi = RAMaddress >> 8
            AddLo = RAMaddress & 0xFF
            dev.write(0x01, [0x11, 0x00, 0x00, AddHi, AddLo])
            USBbuffer = dev.read(0x81, 64)
            RAMaddress += 64
            RAMbuffer.append(USBbuffer)
    # *actual* fastest way of doing it
    return b''.join(RAMbuffer)
