# TODO need to get someone to test this on actual hardware

def MXROMBankSwitch(dev, bankNumber):
    # Convert 16bit bank number to 2 x 8bit numbers
    # Write to address defined under MBC settings to swap banks. This will change depending on certain cart types...
    blo = bankNumber & 0xFF + 0x40
    dev.write(0x01, [0x0A, 0x00, 0x01, 0x3F, 0x00, blo])
    USBbuffer = dev.read(0x81, 64)
    # Probably useless data here...
    return USBbuffer


def dumpMXROM(dev, ROMsize, BankSize, ROMfile):
    num_banks = int(ROMsize/BankSize)
    for bankNumber in range(num_banks):
        print('Dumping ROM:', int(bankNumber*BankSize), ' of ', ROMsize)
        if bankNumber == 0:
            # get bank 0 from address 0, not setbank(0) and get from high bank...
            ROMaddress = 0
        else:
            ROMaddress = BankSize
        MXROMBankSwitch(dev, bankNumber)  # switch to new bank.
        num_banks = BankSize // 64
        for packetNumber in range(num_banks):
            AddHi = ROMaddress >> 8
            AddLo = ROMaddress & 0xFF
            dev.write(0x01, [0x10, 0x00, 0x00, AddHi, AddLo])
            ROMbuffer = dev.read(0x81, 64)
            ROMfile.write(ROMbuffer)
            ROMaddress += 64
