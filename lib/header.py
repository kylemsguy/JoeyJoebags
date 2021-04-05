from abc import ABC, abstractmethod


class Header(ABC):
    @abstractmethod
    def get_rom_size(self):
        pass