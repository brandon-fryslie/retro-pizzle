import os

from game.rom import Rom


class RomCollection:

    def __init__(self, path: str, platform: str):
        self.path = path
        self.platform = platform
        self.roms = self.scan_for_roms(path)

    def scan_for_roms(self, path):
        with os.scandir(path) as entries:
            rom_data = [Rom(entry, self.platform) for entry in entries if entry.is_file()]

        return rom_data

    def __str__(self):
        return ", ".join([str(rom) for rom in self.roms])
