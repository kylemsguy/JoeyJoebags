from ..header import Header


RAMtypes = [0, 2048, 8192, 32768, (32768*4), (32768*2)]

class GBHeader(Header):
    def __init__(self, raw):
        self.raw = raw

    def get_title(self):
        return str(self.raw[0x34:0x43])

    def get_rom_size(self):
        return (32768*(2**(self.raw[0x48])))

    # TODO this could be called get_save_size
    def get_ram_size(self):
        return RAMtypes[self.raw[0x49]]