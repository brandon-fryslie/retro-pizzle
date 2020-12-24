import os
import re
from os import DirEntry


class Rom:

    def __init__(self, fs: DirEntry, platform: str):
        self.fs = fs
        self.title = self.clean_rom_name(fs.name)
        self.platform = platform

    def title(self):
        return

    def clean_rom_name(self, entry: str) -> str:
        filename, extension = os.path.splitext(entry)
        cleaned = re.sub('\(.+\)', '', filename).strip()
        return cleaned

    def __str__(self):
        return f"<Rom[{self.title} ({self.fs.path})]>"

    def __repr__(self):
        return str(self)
