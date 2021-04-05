from .exceptions import FWUpdateLockedException

from ..constants import Command_Get_Version

# TODO Untested right now

def Get_Key_State(dev):
    dev.write(0x01, [0x84])
    USBbuffer = dev.read(0x81, 64)
    return(USBbuffer[0])


def SDID_Read(dev):
    dev.write(0x01, [0x80])
    USBbuffer = dev.read(0x81, 64)
    A = (USBbuffer[0]) + (USBbuffer[1] << 8) + \
        (USBbuffer[2] << 16) + (USBbuffer[3] << 24)
    B = (USBbuffer[4]) + (USBbuffer[5] << 8) + \
        (USBbuffer[6] << 16) + (USBbuffer[7] << 24)
    C = (USBbuffer[8]) + (USBbuffer[9] << 8) + \
        (USBbuffer[10] << 16) + (USBbuffer[11] << 24)
    D = str(hex(A))+","+str(hex(B))+","+str(hex(C))
    return (D)


def update_firmware(dev, fw_data, legacy=False):
    unlocked_state = Get_Key_State(dev) if not legacy else True
    if unlocked_state:
        FWsize = len(fw_data)
        if FWsize == 33280:
            dev.write(0x01, [0x03])
            USBbuffer = dev.read(0x81, 64)
            print("File size correct")
            for FWpos in range(512, 33279, 64):
                dev.write(0x01, fw_data[FWpos:FWpos+64])
            print("Firmware upgrade complete!")
        else:
            raise ValueError("Firmware is invalid")
    else:
        raise FWUpdateLockedException("Non-legacy firmware Update must be unlocked with Key before update can be performed.")


def CheckVersion(dev):
    dev.write(0x01, Command_Get_Version)
    dat = dev.read(0x81, 64)
    sdat = ""
    for x in range(5):
        sdat = sdat+chr(dat[x])
    D = (SDID_Read())
    return sdat, D
