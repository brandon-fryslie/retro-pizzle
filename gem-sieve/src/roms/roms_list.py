import os
from pprint import pprint

import utils
from logs import info_log
from roms.rom_collection import RomCollection


def create_rom_list(base_roms_dir: str, platform: str, output_dir: str):
    output_dir_abs = os.path.abspath(output_dir)

    info_log(f"Creating roms list for platform {platform} from base dir {base_roms_dir}.  Saving to output dir: {output_dir_abs}")
    # create a json list of all the roms

    path = f"{base_roms_dir}/{platform}"

    rc = RomCollection(path, platform)

    roms_list = [rom.title for rom in rc.roms]

    os.makedirs(output_dir_abs, exist_ok=True)
    output_path = f"{output_dir_abs}/rom-list-{platform}.txt"

    info_log(f"Found {len(roms_list)} roms.  Writing to file {output_path}")

    utils.write_file(output_path, "\n".join(roms_list))
