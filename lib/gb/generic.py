from .header import GBHeader
from .common import BV_SetBank, ROMBankSwitch


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
